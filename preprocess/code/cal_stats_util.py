import json
from collections import OrderedDict
from os.path import join, isfile, isdir
import random
import numpy as np
import pandas as pd
import tabulate
import re
from column_info import *

class CalSumStatsUtil(object):
    def __init__(self, dataframe,typeguess):
        assert dataframe is not None, "dataframe can't be None"
        assert typeguess is not None, "typeguess can't be None"

        self.dataframe=dataframe
        self.typeguess=typeguess
        self.colnames = self.dataframe.columns
        self.colcount = len(self.dataframe.columns)



    def cal_sum_stats(self,data,types):
        self.var_dict = {}
        def mode(x, nat):
            out= OrderedDict()
            ux=x.unique()
            tab= pd.crosstab(x.str.match(ux)) #cross check with result

            ColumnInfo.mode= ux[tab.idxmax()]
            ColumnInfo.freqmode= tab.max()

            ColumnInfo.mid=ux[np.where(tab== np.median(tab))][1] # just take the first
            ColumnInfo.fewest= ux[tab.idxmin()]

            ColumnInfo.freqmid= np.median(tab)
            ColumnInfo.freqfewest=min(tab)

            out['mode']=ColumnInfo.mode
            out['freqmode']= ColumnInfo.freqmode
            out['mid']= ColumnInfo.mid
            out['fewest']= ColumnInfo.fewest
            out['freqmid']=ColumnInfo.freqmid
            out['freqfewest']= ColumnInfo.freqfewest

            return out



        for colname in self.colnames:
            col_info = ColumnInfo(colname)
            data_info = self.dataframe[colname]
            """ Doubt here on How to handle types data"""
            nc= types.numchar[np.where(types.varnametypes== self.colnames[colname])]
            nat= types.nature[np.where(types.varnametypes== self.colnames[colname])]

            # data_info= str(data_info)
            data_info=data_info.astype('str')
            valid_data_info=data_info.dropna
            col_info.valid=len(valid_data_info)
            col_info.invalid = len(data_info)-len(valid_data_info)

            data_info.dropna(inplace=True)

            tabs= mode(data_info,nat)

            col_info.mode=tabs.mode
            col_info.freqmode=tabs.freqmode

            col_info.unique= len(data_info.unique()) #unique or uniques

            if(nc== "character"):
                col_info.fewest=tabs.fewest
                col_info.mid= tabs.mid
                col_info.freqfewest= tabs.freqfewest
                col_info.freqmid= tabs.freqmid

                href.t= pd.crosstab(data_info)
                col_info.herfindahl=Herfindahl(herf.t) # concept problem

                col_info.median= None
                col_info.mean= None
                col_info.max=None
                col_info.min=None
                col_info.sd=None

                continue


             #if not character
            data_info = data_info.astype('str')
            col_info.median = np.median(data_info)
            col_info.mean = np.mean(data_info)
            col_info.max = np.max(data_info)
            col_info.min = np.min(data_info)
            col_info.sd = np.std(data_info)

            mode_int=col_info.mode.astype('int')
            col_info.mode=np.around(mode_int,decimals=4).astype('str')

            fewest_int = col_info.fewest.astype('int')
            col_info.fewest = np.around(fewest_int, decimals=4).astype('str')

            mid_int = col_info.mid.astype('int')
            col_info.mid = np.around(mid_int, decimals=4).astype('str')

            freqfewest_int = col_info.freqfewest.astype('int')
            col_info.freqfewest = np.around(freqfewest_int, decimals=4).astype('str')

            freqmid_int = col_info.freqmid.astype('int')
            col_info.freqmid = np.around(freqmid_int, decimals=4).astype('str')

            href.t = pd.crosstab(data_info)
            col_info.herfindahl = Herfindahl(herf.t)  # concept problem

            self.var_dict[colname]=col_info
            continue
        return self.var_dict

        # print()
        for key, val in self.var_dict.items():
            print('col: %s' % key)
            print(json.dumps(val.as_dict(), indent=4))
            # return variable_dict

