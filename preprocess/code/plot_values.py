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
        print("plot values time")
        self.dataframe = dataframe
        self.col_info = col_info
        self.colname = self.col_info.colname
        self.col_series = self.dataframe[self.colname]
        self.histlimit=13
        self.output={}

        self.cal_plot_values(dataframe)

    def ecdf(self,data):
        """Compute ECDF for a one-dimensional array of measurements."""
        # Number of data points: n
        n = len(data)
        # x-data for the ECDF: x
        x = np.sort(data)
        # y-data for the ECDF: y
        y = np.arange(1, n + 1) / n
        print(x, y)
        # Should we return y also?
        return x

    def cal_plot_values(self,dataframe):
        assert dataframe is not None, "dataframe can't be None"

        self.nat= self.col_info.nature
        self.interval= self.col_info.interval

        if(self.nat=="nominal"):
            self.col_series.dropna(inplace=True)
            self.col_series=self.col_series.unique()
            uniques = np.sort(self.col_series)
            lu= len(uniques)
            cdf_func= self.ecdf(self.col_series)
            if(lu<self.histlimit):
                self.output=self.col_series






