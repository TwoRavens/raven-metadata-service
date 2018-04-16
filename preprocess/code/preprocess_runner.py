"""Entrypoint for preprocessing files"""
from collections import OrderedDict
import decimal
import json, time, datetime
import pandas as pd
import os
from os.path import isdir, isfile


import col_info_constants as col_const
from msg_util import msg, msgt, dashes
from np_json_encoder import NumpyJSONEncoder
from type_guess_util import TypeGuessUtil
from summary_stats_util import SummaryStatsUtil
from column_info import ColumnInfo
from plot_values import PlotValuesUtil
from variable_display_util import VariableDisplayUtil
from dataset_level_info_util import DatasetLevelInfo


# Move these elsewhere as things progress ....
# ---------------------------------------------
CSV_FILE_EXT = '.csv'
TAB_FILE_EXT = '.tab'
ACCEPTABLE_FILE_TYPE_EXTS = \
                    (CSV_FILE_EXT,
                     TAB_FILE_EXT)
ACCEPTABLE_EXT_LIST = ', '.join(['"%s"' % x for x in ACCEPTABLE_FILE_TYPE_EXTS])
# ---------------------------------------------

class PreprocessRunner(object):
    """Preprocess relatively small files using pandas"""

    def __init__(self, dataframe, **kwargs):
        """Init with a pandas dataframe"""
        self.df = dataframe
        self.job_id = kwargs.get('job_id', None)
        #self.job_callback_function = kwargs.get('job_callback_function')
        # to populate
        self.variable_info = {} # { variable_name: ColumnInfo, ...}
        self.num_vars = None
        self.num_vars_complete = None

        # for error handling
        self.has_error = False
        self.error_message = None
        ts = time.time()
        self.current_time = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        self.preprocess_id = None

        self.run_preprocess()

    def add_error_message(self, err_msg):
        """Add error message"""
        print(err_msg)
        self.has_error = True
        self.error_message = err_msg

    def update_task_status(self):
        """Optional: update a celery task status"""
        if not self.celery_task:
            # no task available
            return

        if self.num_vars and self.num_vars > 0:
            self.celery_task.update_state(\
                state='PROGRESS',
                meta={'current': self.num_vars_complete,
                      'total': self.num_vars})
            return

        self.add_error_message('Celery update failed')


    def run_preprocess(self):
        """Run preprocess"""
        if not isinstance(self.df, pd.DataFrame):
            self.add_error_message('The dataframe is not valid')
            return False

        if not self.calculate_features():
            return False

        self.run_callback_function()

        return True


    @staticmethod
    def load_from_tabular_file(input_file, **kwargs):
        """Create the dataframe from a tab-delimited file"""
        #job_id = kwargs.get('job_id')
        return PreprocessRunner.load_from_csv_file(\
                                input_file,
                                is_tab_delimited=True,
                                **kwargs)


    @staticmethod
    def load_from_csv_file(input_file, **kwargs):
        """Create the dataframe from a csv file

        kwargs:
            is_tab_delimited - default: False

        success: return PreprocessRunner obj, None
        failure: return None, error message
        """
        #job_id = kwargs.get('job_id')
        if not isfile(input_file):
            return None, 'The file was not found: [%s]' % input_file

        filesize = os.stat(input_file).st_size
        if filesize == 0:
            return None, 'The file size is zero: [%s]' % input_file

        # -----------------------
        # Process kwargs
        # -----------------------
        delimiter = None
        if kwargs.get('is_tab_delimited', False) is True:
            delimiter = '\t'

        #df = pd.read_csv(input_file)
        try:
            df = pd.read_csv(input_file,
                             delimiter=delimiter)
        except pd.errors.ParserError as err_obj:
            err_msg = ('Failed to load csv file (pandas ParserError).'
                       ' \n - File: %s\n - %s') % \
                      (input_file, err_obj)
            return None, err_msg
        except PermissionError as err_obj:
            err_msg = ('No read prermission on this file:'
                       ' \n - File: %s\n - %s') % \
                      (input_file, err_obj)
            return None, err_msg
        except Exception as err_obj:
            err_msg = ('Failed to load csv file.'
                       ' \n - File: %s\n - %s') % \
                      (input_file, err_obj)
            return None, err_msg

        runner = PreprocessRunner(df, **kwargs)

        if runner.has_error:
            return None, runner.error_message

        return runner, None

    @staticmethod
    def load_update_file(preprocess_input, update_input):
        """ Returns the dict from the file input"""
        if not isfile(preprocess_input):
            return None, 'The file was not found: [%s]' % preprocess_input
        elif not isfile(update_input):
            return None, 'The file was not found: [%s]' % update_input

        filesize_preprocess = os.stat(preprocess_input).st_size
        filesize_update = os.stat(update_input).st_size
        if filesize_preprocess == 0:
            return None, 'The file size is zero: [%s]' % preprocess_input

        elif filesize_update == 0:
            return None, 'The file size is zero: [%s]' % update_input


        try:
            preprocess_input_dict = json.loads(preprocess_input, object_pairs_hook=OrderedDict)
        except TypeError as err_obj:
            err_msg = ('Input does not have Ordered dict convertable type'
                       '\n - File: %s\n - %s')% \
                      (preprocess_input, err_obj)
            return None, err_msg
        except Exception as err_obj:
            err_msg = ('Failed to convert into Orderd dict'
                       ' \n - File: %s\n - %s') % \
                      (preprocess_input, err_obj)
            return None, err_msg


        try:
            update_input_dict = json.loads(update_input,
                                           object_pairs_hook=OrderedDict,
                                           parse_float=decimal.Decimal)
        except TypeError as err_obj:
            err_msg = ('Input does not have Ordered dict convertable type'
                       '\n - File: %s\n - %s')% \
                      (update_input, err_obj)
            return None, err_msg
        except Exception as err_obj:
            err_msg = ('Failed to convert into Orderd dict'
                       ' \n - File: %s\n - %s') % \
                      (update_input, err_obj)
            return None, err_msg



        display_util = VariableDisplayUtil(preprocess_input_dict, update_input_dict)

        if display_util.has_error:
            return None, display_util.get_error_messages()

        return display_util, None




    def calculate_features(self):
        """For each variable, calculate summary stats"""
        if self.has_error:
            return False
        # Iterate through data frame and
        # run type guess, cal_stats, and plot_values on each ColumnInfo object
        #
        self.num_vars = len(self.df.columns)
        self.num_vars_complete = 0

        for colnames in self.df:
            # set stats for each column
            col_info = ColumnInfo(colnames)
            col_series = self.df[colnames]

            TypeGuessUtil(col_series, col_info)
            SummaryStatsUtil(col_series, col_info)
            PlotValuesUtil(col_series, col_info)
            #VariableDisplayUtil(col_series, col_info)
            # assign object info to the variable_info
            #
            self.num_vars_complete += 1
            self.variable_info[colnames] = col_info

        # print("completed column", self.num_vars_complete)
        # print(" Number of variable ", self.num_vars)
        return True

    '''
    def add_plot_info(self):
        """For each variable, add plot information as needed"""
        if self.has_error:
            return False

        if not self.variable_info:
            self.add_error_message('Error encountered.  self.variable_info not available')
            return False

        for col_name, col_info in self.variable_info.items():
            # set stats for each column
            PlotValuesUtil(self.df, col_info)

        return True
    '''

    def get_self_section(self):
        """
        {
          "self": {
            "description": "Generated by https://github.com/TwoRavens/raven-metadata-service",
            "created": "current timestamp", # job.modified when done via the web
            "preprocess_id": 45  # null for now; job.id when done via the web
            "version": 1 # subsequent updates will increment this number
        },
        """
        self_section = OrderedDict()
        self_section['description'] = \
            ('Generated by https://github.com/TwoRavens/raven-metadata-service')
        self_section['created'] = self.current_time
        self_section[col_const.PREPROCESS_ID] = self.job_id
        self_section['version'] = 1

        return self_section

    def get_dataset_level_info(self):
        """
        "dataset": {
       "row_cnt": 1000,
       "variable_cnt": 25
                }

        """
        dataset_level = OrderedDict()
        #print("data frame to pass ", self.df)
        dataset_level_info = DatasetLevelInfo(self.df);
        if dataset_level_info.has_error:
            dataset_level = {"error": dataset_level_info.error_messages}
            return dataset_level

        dataset_level = dataset_level_info.final_output
        return dataset_level




    def show_final_info(self):
        """Print the final info to the screen"""
        if self.has_error:
            err_msg = ('An error occurred earlier in the process:\n%s') % \
                      self.error_message
            print(err_msg)
            return

        info_string = self.get_final_dict(as_string=True)

        print(info_string)



    def get_final_json_indented(self, indent=4):
        """Return the final variable info as a JSON string"""
        if self.has_error:
            err_msg = ('An error occurred earlier in the process:\n%s') % \
                      self.error_message
            print(err_msg)
            return

        return self.get_final_dict(as_string=True,
                                   indent=indent)


    def get_final_json(self, indent=None):
        """Return the final variable info as a JSON string"""
        if self.has_error:
            err_msg = ('An error occurred earlier in the process:\n%s') % \
                      self.error_message
            print(err_msg)
            return

        return self.get_final_dict(as_string=True,
                                   indent=indent)



    def get_final_dict(self, as_string=False, **kwargs):
        """Return the preprocess data as an OrderedDict"""
        if self.has_error:
            err_msg = ('An error occurred earlier in the process:\n%s') % \
                      self.error_message
            print(err_msg)
            return


        fmt_variable_info = OrderedDict()   # capture the variables section
        fmt_display_variable_info = OrderedDict()   # capture the variable_display section
        fmt_display_variable_info['editable'] = ColumnInfo.get_editable_column_labels()
        # Iterate through each column and pull variable + variable_display info
        #
        for col_name, col_info in self.variable_info.items():
            # col_info.print_values()
            fmt_variable_info[col_name] = col_info.as_dict()
            fmt_display_variable_info[col_name] = VariableDisplayUtil.get_default_settings()

        # Format the entire document
        #
        overall_dict = OrderedDict()

        overall_dict[col_const.SELF_SECTION_KEY] = self.get_self_section() # add the "self" section

        overall_dict[col_const.DATASET_LEVEL_KEY] = self.get_dataset_level_info() # add "dataset" section
        overall_dict[col_const.VARIABLES_SECTION_KEY] = fmt_variable_info   # add "variables"

        overall_dict[col_const.VARIABLE_DISPLAY_SECTION_KEY] = fmt_display_variable_info

        if as_string:
            # Convert the OrderedDict to a JSON string
            #
            indent_level = kwargs.get('indent', 4)
            if indent_level is None:
                pass
            elif (not isinstance(indent_level, int)) or indent_level > 50:
                indent_level = 4

            return json.dumps(overall_dict,
                              indent=indent_level,
                              cls=NumpyJSONEncoder)

        # w/o this step, a regular json.dumps() fails on the returned dict
        #
        jstring = json.dumps(overall_dict,
                             cls=NumpyJSONEncoder)
        return json.loads(jstring,
                          object_pairs_hook=OrderedDict,
                          parse_float=decimal.Decimal)
