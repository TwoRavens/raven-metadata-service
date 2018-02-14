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
        self.col_series = dataframe[self.colname]

        self.calc_stats(self.dataframe)

    def calc_stats(self, dataframe):
        self.col_series.dropna(inplace=True)

        # --------------------------
        # similar to preprocess.R "Mode" function
        # --------------------------
        self.col_info.uniques = len(self.col_series.unique())
        col_val = None
        val_cnt = None
        mid_pt = int(self.col_info.uniques / 2)

        # iterate through value_counts for mode stats
        #
        row_num = 0
        for col_val, val_cnt in self.col_series.value_counts().iteritems():
            row_num += 1
            if row_num == 1:
                self.col_info.mode = col_val
                self.col_info.freqmode = val_cnt
            if row_num == mid_pt:
                self.col_info.mid = col_val
                self.col_info.freqmid = val_cnt

        self.col_info.fewest = col_val
        self.col_info.freqfewest = val_cnt



        if self.col_info.is_character():

            # self.col_info.herfindahl=self.herfindahl_index(self.col_series)
            self.col_info.median = NOT_APPLICABLE
            self.col_info.max = NOT_APPLICABLE
            self.col_info.min = NOT_APPLICABLE
            self.col_info.mean = NOT_APPLICABLE
            self.col_info.std_dev = NOT_APPLICABLE



        elif self.col_info.is_numeric():

            self.col_info.median = self.col_series.median()
            self.col_info.max = self.col_series.max()
            self.col_info.min = self.col_series.min()
            self.col_info.mean = self.col_series.mean()
            self.col_info.std_dev = self.col_series.std()
            self.col_info.herfindahl = self.herfindahl_index(self.col_series)

            self.col_info.mode = np.around(self.col_info.mode,4)
            self.col_info.fewest = np.around(self.col_info.fewest, 4)
            self.col_info.mid = np.around(self.col_info.mid, 4)
            # freqfewest and freqmid left for now as they always give int value. why SignIf then?
            # print("--"*20)
            # print("name : ", self.col_info.colname)
            # print("mode : ", self.col_info.mode)
            # print("fewest : ", self.col_info.fewest)
            # print("mid : ", self.col_info.mid)

    def herfindahl_index(self,col_data):
        # check again with the logic of calculating, what values are squared
        """
        Calculate Herfindahl-Hirschman Index (HHI) for the column data.
        For each given day, HHI is defined as a sum of squared weights of
        %values in a col_series; and varies from 1/N to 1.
        """
        # s = pd.Series([4, 8, 12])
        col_data.dropna(inplace=True)
        totalSum = sum(col_data)
        fract = []
        for val, cnt in col_data.items():
            fract.append(np.math.pow(cnt / totalSum, 2))

        return sum(fract)



