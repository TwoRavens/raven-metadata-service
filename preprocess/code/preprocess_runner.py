"""Entrypoint for preprocessing files"""
from collections import OrderedDict
import json
from os.path import isdir, isfile
import pandas as pd

from msg_util import msg, msgt, dashes
from np_json_encoder import NumpyJSONEncoder
from type_guess_util import TypeGuessUtil
from summary_stats_util import SummaryStatsUtil
from column_info import ColumnInfo
from plot_values import PlotValuesUtil

class PreprocessRunner(object):
    """Preprocess relatively small files using pandas"""

    def __init__(self, dataframe):
        """Init with a pandas dataframe"""
        self.df = dataframe

        # to populate
        self.variable_info = {} # { variable_name: ColumnInfo, ...}

        # for error handling
        self.has_error = False
        self.error_message = None

        self.run_preprocess()

    def add_error_message(self, err_msg):
        """Add error message"""
        print(err_msg)
        self.has_error = True
        self.error_message = err_msg


    def run_preprocess(self):
        """Run preprocess"""
        if not isinstance(self.df, pd.DataFrame):
            self.add_error_message('The dataframe is not valid')
            return False

        if not self.create_variable_info():
            return False

        if not self.calculate_stats():
            return False

        return True

    @staticmethod
    def load_from_csv_file(input_file):
        """Create the dataframe from a file

        success: return PreprocessRunner obj, None
        faile: return None, error message
        """
        if not isfile(input_file):
            return None, 'file not found: %s' % input_file

        #df = pd.read_csv(input_file)
        try:
            df = pd.read_csv(input_file)
        except pd.errors.ParserError as err_obj:
            err_msg = ('Failed to load csv file (pandas ParserError).'
                       ' \n - File: %s\n - %s') % \
                      (input_file, err_obj)
            return None, err_msg
        except Exception as err_obj:
            err_msg = ('Failed to load csv file.'
                       ' \n - File: %s\n - %s') % \
                      (input_file, err_obj)
            return None, err_msg

        runner = PreprocessRunner(df)

        if runner.has_error:
            return None, runner.error_message

        return runner, None



    def create_variable_info(self):
        """Use typeguess to produce initial variable info"""
        if self.has_error:
            return False

        # Use the TypeGuessUtil to produce variable_info
        #
        type_guess_util = TypeGuessUtil(self.df)

        self.variable_info = type_guess_util.get_variable_dict()

        if not self.variable_info:
            self.add_error_message('Error encountered during TypeGuess process')
            return False

        return True


    def calculate_stats(self):
        """For each variable, calculate summary stats"""
        if self.has_error:
            return False

        if not self.variable_info:
            self.add_error_message('Error encountered.  self.variable_info not available')
            return False

        # Iterate through variable info and
        # run calc stats on each ColumnInfo object
        #
        for col_name, col_info in self.variable_info.items():
            # set stats for each column
            col_series = self.df[col_name]
            SummaryStatsUtil(col_series, col_info)
            PlotValuesUtil(col_series, col_info)

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

    def show_final_info(self):
        """Print the final info to the screen"""
        if self.has_error:
            err_msg = ('An error occurred earlier in the process:\n%s') % \
                      self.error_message
            print(err_msg)
            return

        info_string = self.get_final_dict(as_string=True)

        print(info_string)


    def get_final_json(self, indent=4):
        """Return the final variable info as a JSON string"""
        if self.has_error:
            err_msg = ('An error occurred earlier in the process:\n%s') % \
                      self.error_message
            print(err_msg)
            return

        return self.get_final_dict(as_string=True,
                                   indent=indent)


    def get_final_dict(self, as_string=False, **kwargs):
        """Return the final variable info as an OrderedDict"""
        if self.has_error:
            err_msg = ('An error occurred earlier in the process:\n%s') % \
                      self.error_message
            print(err_msg)
            return

        fmt_variable_info = OrderedDict()
        for col_name, col_info in self.variable_info.items():
            col_info.print_values()
            fmt_variable_info[col_name] = col_info.as_dict()

        overall_dict = OrderedDict()
        overall_dict['variables'] = fmt_variable_info


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

        return overall_dict


    def get_formatted_dict(self):
        """Return an OrderedDict containing the final values"""
        if self.has_error:
            return False, "An error occurred earlier in the process"

        fmt_variable_info = OrderedDict()
        for col_name, col_info in self.variable_info.items():
            col_info.print_values()
            fmt_variable_info[col_name] = col_info.as_dict()

        overall_dict = OrderedDict()
        overall_dict['variables'] = fmt_variable_info
        variable_string = json.dumps(overall_dict, indent=4, cls=MyEncoder)
        print(variable_string)
        file_name = join(OUTPUT_DIR, 'variable_output_testfile1.json')
        open(file_name, 'w').write(variable_string)
        print('file written: %s' % file_name)
