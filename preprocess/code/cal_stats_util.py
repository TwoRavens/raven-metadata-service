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
        print(self.col_info.colname)
        print(self.col_info.mode)
        print(self.col_info.freqmode)
        print(self.col_info.uniques)
        print(self.col_info.valid)
        print(self.col_info.invalid)
        print(self.col_info.median)
        print(self.col_info.max)
        print(self.col_info.mid)
        print(self.col_info.min)
        print(self.col_info.sd)
        print(self.col_info.mean)
        print(self.col_info.herfindahl)



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


                #
    # def cal_sum_stats(self,data,types):
    #     self.var_dict = {}
    #
    #
    #     for colname in self.colnames:
    #         col_info = ColumnInfo(colname)
    #         data_info = self.dataframe[colname]
    #         """ Doubt here on How to handle types data"""
    #         nc= types.numchar[np.where(types.varnametypes== self.colnames[colname])]
    #         nat= types.nature[np.where(types.varnametypes== self.colnames[colname])]
    #
    #         # data_info= str(data_info)
    #         data_info=data_info.astype('str')
    #         valid_data_info=data_info.dropna
    #         col_info.valid=len(valid_data_info)
    #         col_info.invalid = len(data_info)-len(valid_data_info)
    #
    #         data_info.dropna(inplace=True)
    #
    #         tabs= mode(data_info,nat)
    #
    #         col_info.mode=tabs.mode
    #         col_info.freqmode=tabs.freqmode
    #
    #         col_info.unique= len(data_info.unique()) #unique or uniques
    #
    #         if(nc== "character"):
    #             col_info.fewest=tabs.fewest
    #             col_info.mid= tabs.mid
    #             col_info.freqfewest= tabs.freqfewest
    #             col_info.freqmid= tabs.freqmid
    #
    #             href.t= pd.crosstab(data_info)
    #             col_info.herfindahl=Herfindahl(herf.t) # concept problem
    #
    #             col_info.median= None
    #             col_info.mean= None
    #             col_info.max=None
    #             col_info.min=None
    #             col_info.sd=None
    #
    #             continue
    #
    #
    #          #if not character
    #         data_info = data_info.astype('str')
    #         col_info.median = np.median(data_info)
    #         col_info.mean = np.mean(data_info)
    #         col_info.max = np.max(data_info)
    #         col_info.min = np.min(data_info)
    #         col_info.sd = np.std(data_info)
    #
    #         mode_int=col_info.mode.astype('int')
    #         col_info.mode=np.around(mode_int,decimals=4).astype('str')
    #
    #         fewest_int = col_info.fewest.astype('int')
    #         col_info.fewest = np.around(fewest_int, decimals=4).astype('str')
    #
    #         mid_int = col_info.mid.astype('int')
    #         col_info.mid = np.around(mid_int, decimals=4).astype('str')
    #
    #         freqfewest_int = col_info.freqfewest.astype('int')
    #         col_info.freqfewest = np.around(freqfewest_int, decimals=4).astype('str')
    #
    #         freqmid_int = col_info.freqmid.astype('int')
    #         col_info.freqmid = np.around(freqmid_int, decimals=4).astype('str')
    #
    #         href.t = pd.crosstab(data_info)
    #         col_info.herfindahl = Herfindahl(herf.t)  # concept problem
    #
    #         self.var_dict[colname]=col_info
    #         continue
    #
    #
    #     # print()
    #     for key, val in self.var_dict.items():
    #         print('col: %s' % key)
    #         print(json.dumps(val.as_dict(), indent=4))
    #         # return variable_dict
