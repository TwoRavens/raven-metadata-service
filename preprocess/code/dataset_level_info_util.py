""" this is the information of dataset level info"""
import numpy as np
import pandas as pd
import re
from np_json_encoder import NumpyJSONEncoder
from collections import OrderedDict

class DatasetLevelInfo(object):
    def __init__(self, df):
        """This class sets the dataset level info of the preprocess file. """
        #print(" df for dataset level info *** : ", df)
        self.dataframe = df
        self.rows_count = None
        self.variables_count = None
        self.has_error = False
        self.error_messages = []
        self.final_output = {}

        self.set_values()

    def set_values(self):
        """
        "dataset": {
       "row_cnt": 1000,
       "variable_cnt": 25
            }
        """
        if self.dataframe is not None:
            self.rows_count = self.dataframe.shape[0] # shape[0] gives the number of records/rows and is faster then count
            self.variables_count = len(self.dataframe.columns)
        else:
            self.has_error = True
            self.error_messages.append(" There is no data available to get dataset level info")
            return
        if self.rows_count < 1:
            self.has_error = True
            self.error_messages.append(" This is an empty dataframe with no record")
            return
        if self.variables_count < 1:
            self.has_error = True
            self.error_messages.append(" This is an empty dataframe with no variables")
            return


        self.final_output = dict(row_cnt=self.rows_count,
                                 variable_cnt=self.variables_count)


        # print("*** final output for dataset level info", self.final_output)
