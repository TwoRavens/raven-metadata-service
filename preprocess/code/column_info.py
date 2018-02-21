"""Module for preprocess structure"""

from collections import OrderedDict
import json
import pandas as pd
from col_info_constants import \
    (NUMCHAR_NUMERIC, NUMCHAR_CHARACTER)


class ColumnInfo(object):
    """Sets up the expected structure of the whole preprocess output file"""

    def __init__(self, colname):
        """Init with column name"""
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


    def is_numeric(self):
        # is this NUMCHAR_NUMERIC?
        return self.numchar_val == NUMCHAR_NUMERIC

    def is_character(self):
        # is this NUMCHAR_CHARACTER?
        return self.numchar_val == NUMCHAR_CHARACTER


    def get_variable_labels(self):
        """Set labels for variable output"""
        label_list = (
            ('varnameSumStat', self.colname),
            ('plotvalues', self.plot_values),
            ('plottype', self.plot_type),
            ('plotx', self.plotx),
            ('ploty', self.ploty),
            ('cdfplottype', self.cdf_plottype),
            ('cdfplotx', self.cdf_plotx),
            ('cdfploty', self.cdf_ploty),
            ('labl', self.labl),
            ('median', self.median),
            ('mean', self.mean),
            ('mode', self.mode[:5]),
            ('max', self.max),
            ('min', self.min),
            ('invalid', self.invalid),
            ('valid', self.valid),
            ('sd', self.std_dev),
            ('uniques', self.uniques),
            ('herfindahl', self.herfindahl),
            ('freqmode', self.freqmode),
            ('fewest', self.fewest[:3]),
            ('mid', self.mid),
            ('freqfewest', self.freqfewest),
            ('freqmid', self.freqmid),
            ('numchar', self.numchar_val),
            ('nature', self.nature),
            ('binary', self.binary),
            ('interval', self.default_interval),
            ('time', self.time_val),
            ('defaultInterval', self.default_interval),
            ('defaultNumchar', self.numchar_val),
            ('defaultNature', self.nature),
            ('defaultBinary', self.binary),
            ('defaultTime', self.time_val),
            )
        # print("-"*20)
        # print(label_list)
        return label_list

    def print_values(self):
        """print to screen"""
        print('---- %s ----' % self.colname)
        for label, val in self.get_variable_labels():
            print('%s: %s' % (label, val))

    def as_dict(self, as_string=False):
        """For final output"""
        ordered_dict = OrderedDict()

        for label, val in self.get_variable_labels():
            ordered_dict[label] = val

        if as_string:
            return json.dumps(ordered_dict)

        return ordered_dict
