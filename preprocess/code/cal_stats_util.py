import json
from collections import OrderedDict
from os.path import join, isfile, isdir
import random
import numpy as np
import pandas as pd
#import tabulate
import re
from column_info import *
from col_info_constants import *
from type_guess_util import *

class CalSumStatsUtil(object):
    def __init__(self, dataframe, col_info):
        assert dataframe is not None, "dataframe can't be None"
        assert col_info is not None, "col_info can't be None"

        self.dataframe = dataframe
        self.col_info = col_info
        self.colname = self.col_info.colname
        self.col_series = self.dataframe[self.colname]


        # self.stats_var={}
        # print('col_info',self.col_info)
        self.calc_stats(self.dataframe)



    def calc_stats(self,dataframe):

        self.col_info.invalid = dataframe[self.colname].isnull().sum()
        self.col_info.valid = dataframe[self.colname].count()

        dataframe[self.colname].dropna(inplace=True)

        self.col_info.uniques=len(dataframe[self.colname].unique())

        if self.col_info.is_character():

            self.col_info.herfindahl='?'
            self.col_info.median = NOT_APPLICABLE
            self.col_info.max = NOT_APPLICABLE
            self.col_info.min = NOT_APPLICABLE
            self.col_info.mean = NOT_APPLICABLE
            self.col_info.sd = NOT_APPLICABLE

        elif self.col_info.is_numeric():

            self.col_info.median = self.col_series.median()
            self.col_info.max = self.col_series.max()
            self.col_info.min = self.col_series.min()
            self.col_info.mean = self.col_series.mean()
            self.col_info.sd = self.col_series.std()
            self.col_info.herfindahl = '?'

        # --------------------------
        # similar to preprocess.R "Mode" function
        # --------------------------
        col_val = None
        val_cnt = None
        mid_pt = int(self.col_info.uniques / 2)

        # iterate through value_counts for mode stats
        #
        row_num = 0
        for col_val, val_cnt in dataframe[self.colname].value_counts().iteritems():
            row_num += 1
            if row_num == 1:
                self.col_info.mode = col_val
                self.col_info.freqmode = val_cnt
            if row_num == mid_pt:
                self.col_info.mid = col_val
                self.col_info.freqmid = val_cnt


        self.col_info.fewest = col_val
        self.col_info.freqfewest = val_cnt
