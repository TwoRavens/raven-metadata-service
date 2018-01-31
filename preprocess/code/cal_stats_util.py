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


        # print('dataframe passed', dataframe[self.colname])


        self.col_info.invalid = dataframe[self.colname].isnull().sum()
        self.col_info.valid = dataframe[self.colname].count()

        dataframe[self.colname].dropna(inplace=True)
        tabs= self.set_mode_stats(dataframe[self.colname])

        self.col_info.mode = 1
        self.col_info.freqmode= 1

        self.col_info.uniques=len(dataframe[self.colname].unique())




        if self.col_info.is_character():
            #self.col_info.fewest = # from mode, etc
            self.col_info.fewest=2
            self.col_info.mid=2
            self.col_info.freqfewest=2
            self.col_info.freqmid= 2
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

            if self.col_info.uniques:
                freq_cnt = None
                mid_pt = int(self.col_info.uniques / 2)

                for idx, freq_cnt in enumerate(dataframe[self.colname].value_counts().iteritems(), 1):
                    if idx == 1:
                        self.col_info.mode, self.col_info.freqmode = freq_cnt
                    if idx == mid_pt:
                        self.col_info.mid, self.col_info.freqmid = freq_cnt

                        self.col_info.fewest, self.col_info.freqfewest = freq_cnt

        print("-" * 40)
        print("varnameTypes :",self.col_info.colname)
        print("defaultInterval :",self.col_info.default_interval)
        print("defaultNumchar :",self.col_info.numchar_val)
        print("defaultNature :",self.col_info.nature)
        print("defaultBinary :",self.col_info.binary)
        print("defaultTime :",self.col_info.time_val)
        print("mode :",self.col_info.mode)
        print("freqmode :",self.col_info.freqmode)
        print("uniques :",self.col_info.uniques)
        print("valid :",self.col_info.valid)
        print("invalid :",self.col_info.invalid)
        print("median :",self.col_info.median)
        print("max :",self.col_info.max)
        print("mid :",self.col_info.mid)
        print("min :",self.col_info.min)
        print("sd :",self.col_info.sd)
        print("mean :",self.col_info.mean)
        print("fewest :", self.col_info.fewest)
        print("freqfewest :", self.col_info.freqfewest)
        print("freqmid :", self.col_info.freqmid)
        print("herfindahl :",self.col_info.herfindahl)
        # self.stats_var[self.colname]=self.col_info




    def set_mode_stats(self, data):

        self.nat = self.col_info.nature  # reference to nature

        out = OrderedDict()
        # ux = data.unique()
        # tab = pd.crosstab(data.str.match(ux))  # cross check with result
        # print('this is tab', tab)
        # ColumnInfo.mode = ux[tab.idxmax()]
        # ColumnInfo.freqmode = tab.max()
        #
        # ColumnInfo.mid = ux[np.where(tab == np.median(tab))][1]  # just take the first
        # ColumnInfo.fewest = ux[tab.idxmin()]
        #
        # ColumnInfo.freqmid = np.median(tab)
        # ColumnInfo.freqfewest = min(tab)

        out['mode'] = 1
        out['freqmode'] = 1
        out['mid'] = 1
        out['fewest'] = 1
        out['freqmid'] = 1
        out['freqfewest'] = 1

        return out
