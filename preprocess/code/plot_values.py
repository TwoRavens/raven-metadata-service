import json
from collections import OrderedDict
from os.path import join, isfile, isdir
import random
import numpy as np
import pandas as pd


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
        self.cdfx=None
        self.cdfy=None
    def ecdf(self,data):
        """Compute ECDF for a one-dimensional array of measurements."""
        # Number of data points: n
        n = len(data)
        # x-data for the ECDF: x
        x = np.sort(data)
        # y-data for the ECDF: y
        y=np.arange(1, n + 1) / n

        # print(x, y)
        # Should we return x also? though it is just sorted array
        return y

    def cal_plot_values(self,dataframe):
        assert dataframe is not None, "dataframe can't be None"

        nat = self.col_info.nature
        print(nat)
        myint= self.col_info.interval
        self.plot_values=list()
        if nat!= NATURE_NOMINAL:

            self.col_series.dropna(inplace=True)
            uniques = np.sort(self.col_series.unique())
            lu= len(uniques)
            cdf_func= self.ecdf(self.col_series)
            if(lu<self.histlimit):
                print("into it")
                #code for plot values
                self.col_info.plot_type= PLOT_BAR

                for val,cnt in self.col_series.value_counts().iteritems():
                    if type(val) is not str:
                        try:
                            self.output[str(val)] = cnt
                        except:
                            try:
                                self.output[repr(val)] = cnt
                            except:
                                pass
                        del cnt


                self.col_info.plot_values=self.output

                #code for cdf values
                self.cdfx=np.sort(uniques)
                self.col_info.cdf_plottype = PLOT_BAR
                self.col_info.cdf_plotx=np.linspace(start=min(self.cdfx), stop=max(self.cdfx), num=len(self.cdfx))
                self.col_info.cdf_ploty=self.ecdf(self.cdfx)


            else:
                    #code for plot values
                    self.col_info.plot_type= PLOT_CONTINUOUS
                    # here the code for plotx and ploty comes using r density function

                    #code for cdf values
                    self.col_info.cdf_plottype = PLOT_CONTINUOUS
                    if lu >= 50 or (lu <50 and myint != INTERVAL_DISCRETE):
                        self.col_info.cdf_plotx=np.linspace(start=min(self.col_series), stop=max(self.col_series), num=50)

                    else:
                        self.col_info.cdf_plotx = np.linspace(start=min(self.col_series), stop=max(self.col_series),
                                                              num=lu)




                    self.col_info.cdf_ploty=self.ecdf(self.col_info.cdf_plotx)

        else:
            """Here data nature is not nominal"""
            #code for plot values
            self.col_info.plot_type = PLOT_BAR

            for val, cnt in self.col_series.value_counts().iteritems():
                if type(val) is not str:
                    try:
                        self.output[str(val)] = cnt
                    except:
                        try:
                            self.output[repr(val)] = cnt
                        except:
                            pass
                    del cnt

            self.col_info.plot_values = self.output

            #code for cdf values
            self.col_info.cdf_plottype=None
            self.col_info.cdf_plotx=None
            self.col_info.cdf_ploty=None


        # if metadataflag  !=1
        self.col_info.labl=""
















