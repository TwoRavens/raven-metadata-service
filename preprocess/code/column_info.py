"""Module for preprocess structure"""

from collections import OrderedDict
import json
import pandas as pd
from np_json_encoder import NumpyJSONEncoder
from col_info_constants import \
    (NUMCHAR_NUMERIC, NUMCHAR_CHARACTER)


class ColumnInfo(object):
    """Sets up the expected structure of the whole preprocess output file"""

    def __init__(self, colname):
        """Init with column name"""
        # -------------
        # self data
        # -------------

        self.schema = None
        self.description = None
        self.created = None
        self.preprocess_id = None
        self.data_url = None
        self.format = None
        self.preprocess_version = None
        self.schema_version = None

        # -------------
        # more general
        # -------------
        self.colname = colname
        self.valid = None
        self.invalid = None

        # ----------------------
        # Type Guess Info
        # ----------------------
        self.numchar_val = None
        self.default_interval = None
        self.nature = None
        self.time_val = None
        self.binary = None

        # set at type util
        self.varnames_sum_stat = None

        # Stats Info
        self.mode = []
        self.freqmode = None
        self.mid = None
        self.fewest = []
        self.freqmid = None
        self.freqfewest = None
        self.median = None
        self.mean = None
        self.max = None
        self.min = None
        self.std_dev = None
        self.herfindahl = None

        self.uniques = None

        self.numchar = None
        self.nature = None
        self.binary = None
        self.interval = None
        self.time = None


        #plot vlaues
        self.plot_values = {}
        self.plot_type = None
        self.plotx = None
        self.ploty = None
        self.cdf_plottype = None
        self.cdf_plotx = None
        self.cdf_ploty = None
        self.labl = None


        # ----------------------
        # variable_display Info
        # ----------------------
        self.variable_display = {}
        self.editable = [
         "label",
         "varSumState"
        ]
        self.viewable = None
        self.omit = []
        self.images = {}

    def is_numeric(self):
        # is this NUMCHAR_NUMERIC?
        return self.numchar_val == NUMCHAR_NUMERIC

    def is_character(self):
        # is this NUMCHAR_CHARACTER?
        return self.numchar_val == NUMCHAR_CHARACTER

    def get_numeric_attribute_names(self):
        """These attributes, when set, are always numeric.  Ex/ mean, median, etc."""

        return  ('invalid', 'valid', 'uniques',
                 'median', 'mean', 'max', 'min',
                 'freqmode', 'freqfewest', 'freqmid',
                 'std_dev', 'herfindahl',
                 'plot_values', 'plotx', 'ploty',
                 'cdf_plotx', 'cdf_ploty')

    def is_numeric_attribute(self, ye_attr_name):
        """Test if the attribute is numeric (or null if not set)"""
        if ye_attr_name in self.get_numeric_attribute_names():
            return True
        return False

    def get_display_variables_labels(self):
        pass

    def get_self_variables_labels(self):
        pass

    def get_variable_labels(self):
        """Set labels for variable output.  List of (label, variable name)
        Example of iterating through to show labels and values:
            ```
            for label, varname in self.get_variable_labels():
                variable_val = self.__dict__.get(varname)
                print('%s: %s' % (label, variable_val))
            ```
        """
        label_list = (
            ('varnameSumStat', 'colname'),
            ('labl', 'labl'),

            ('numchar', 'numchar_val'),
            ('nature', 'nature'),
            ('binary', 'binary'),
            ('interval', 'default_interval'),
            ('time', 'time_val'),

            ('invalid', 'invalid'),
            ('valid', 'valid'),
            ('uniques', 'uniques'),

            ('median', 'median'),
            ('mean', 'mean'),
            ('max', 'max'),
            ('min', 'min'),

            ('mode', 'mode[:5]'),
            ('freqmode', 'freqmode'),
            ('fewest', 'fewest[:3]'),
            ('freqfewest', 'freqfewest'),
            ('mid', 'mid'),
            ('freqmid', 'freqmid'),

            ('sd', 'std_dev'),
            ('herfindahl', 'herfindahl'),

            ('plotvalues', 'plot_values'),
            ('plottype', 'plot_type'),
            ('plotx', 'plotx'),
            ('ploty', 'ploty'),
            ('cdfplottype', 'cdf_plottype'),
            ('cdfplotx', 'cdf_plotx'),
            ('cdfploty', 'cdf_ploty'),

            ('defaultInterval', 'default_interval'),
            ('defaultNumchar', 'numchar_val'),
            ('defaultNature', 'nature'),
            ('defaultBinary', 'binary'),
            ('defaultTime', 'time_val'),
            )
        # print("-"*20)
        # print(label_list)
        return label_list

    def print_values(self):
        """print to screen"""
        print('---- %s ----' % self.colname)
        for label, varname in self.get_variable_labels():
            print('%s: %s' % (label, self.__dict__.get(varname)))

    def as_dict(self, as_string=False):
        """For final output"""
        ordered_dict = OrderedDict()

        for label, varname in self.get_variable_labels():
            ordered_dict[label] = self.__dict__.get(varname)

        if as_string:
            return json.dumps(ordered_dict, cls=NumpyJSONEncoder)

        return ordered_dict

    def get_variable_display_dict(self, as_string=False):
        """For final output"""
        ordered_dict = OrderedDict()

        for label, varname in self.get_display_variables_labels():
            ordered_dict[label] = self.__dict__.get(varname)

        if as_string:
            return json.dumps(ordered_dict, cls=NumpyJSONEncoder)

        return ordered_dict

    def get_self_variables_dict(self, as_string=False):
        """For final output"""
        ordered_dict = OrderedDict()

        for label, varname in self.get_self_variables_labels():
            ordered_dict[label] = self.__dict__.get(varname)

        if as_string:
            return json.dumps(ordered_dict, cls=NumpyJSONEncoder)

        return ordered_dict