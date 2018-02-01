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

class PlotValuesUtil(object):
    def __init__(self, dataframe, col_info):
        assert dataframe is not None, "dataframe can't be None"
        assert col_info is not None, "col_info can't be None"

        self.dataframe = dataframe
        self.col_info = col_info
        self.colname = self.col_info.colname
        self.col_series = self.dataframe[self.colname]
        self.histlimit=13

    def cal_plot_values(self,dataframe):
        assert dataframe is not None, "dataframe can't be None"

        self.nat= self.col_info.nature
        self.interval= self.col_info.interval

        if(self.nat=="nominal"):
            self.col_series.dropna(inplace=True)
            uniques = self.col_series.sort_values((self.col_series.unique()))
            lu= len(uniques)



