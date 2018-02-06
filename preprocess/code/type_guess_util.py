import json
from collections import OrderedDict
from os.path import join, isfile, isdir
import random
import numpy as np
import pandas as pd

from col_info_constants import *
from column_info import *


class TypeGuessUtil(object):
    """Check variable types of a dataframe"""
    def __init__(self, dataframe):
        """Init with a pandas dataframe"""
        assert dataframe is not None, "dataframe can't be None"

        self.dataframe = dataframe
        self.colnames = self.dataframe.columns
        self.colcount = len(self.dataframe.columns)
        # print("data frame")
        # print(self.dataframe)
        # print("colnames")
        # print(self.colnames)
        # final output


        # { col_name : ColumnInfoObject, col_name : ColumnInfoObject}
        self.variable_dict = {}

        # # final outout returned
        self.check_types()

    def get_variable_dict(self):
        """Return the calculated results"""
        return self.variable_dict

    def get_variable_count(self):
        """Return the number of variables with type info"""
        return len(self.variable_dict.keys())

    def check_types(self):
        """check the types of the dataframe"""
        #print(self.colnames)
        #assert self.colnames, 'self.colnames must have values'

        '''
        self.colname=None
        self.numchar_val = None
        self.default_interval = None
        self.nature = None
        self.time_val = None
        self.binary = None
        '''
        # Iterate though variables and set type info
        for colname in self.colnames:
            col_info = ColumnInfo(colname)

            # print(colname)
            data_info= self.dataframe[colname]
            # print("data_info")
            # print(data_info)
            # print(type(data_info))
            # set time
            col_info.time_val = self.check_time(data_info)

            # set vals if factor or logical
            #

            # print("******")
            if self.is_not_numeric(data_info) or \
                self.is_logical(data_info):

                col_info.numchar_val = NUMCHAR_CHARACTER
                col_info.default_interval = INTERVAL_DISCRETE
                col_info.nature = NATURE_NOMINAL

                # print(col_info.numchar_val)
                # print(col_info.default_interval)
                # print(col_info.nature)

                data_info.dropna(inplace=True)
                if (len(data_info.unique()) == 2):
                    # print("#2")
                    col_info.binary = BINARY_YES
                    # print(col_info.binary)
                else:
                    col_info.binary = BINARY_NO

                self.variable_dict[colname] = col_info

                continue    # go onto next column

            # Drop nulls...
            data_info.dropna(inplace=True)

            data_info=data_info.astype('int')
            # print(data_info)

            if (len(data_info.unique()) == 2):
                col_info.binary = BINARY_YES
            else:
                col_info.binary = BINARY_NO

            if any(data_info.isnull()):
                # DOES IT EVER REACH? AFTER earlier .dropna...
                col_info.numchar_val = NUMCHAR_CHARACTER
                col_info.nature = NATURE_NOMINAL
                col_info.default_interval = INTERVAL_DISCRETE
                # print("#3")
                # print(col_info.numchar_val)
                # print(col_info.default_interval)
                # print(col_info.nature)
            else:
                col_info.numchar_val = NUMCHAR_NUMERIC
                # print("#4")
                # print(col_info.numchar_val)

                if self.check_decimal(data_info):
                    col_info.default_interval = INTERVAL_CONTINUOUS
                    col_info.nature = self.check_nature(data_info, True)
                    # print("#5")
                    # print(col_info.nature)
                else:
                    col_info.default_interval = INTERVAL_DISCRETE
                    col_info.nature = self.check_nature(data_info, False)
                    # print("#6")
                    # print(col_info.nature)


            # some other stuff, dropna
            # ColumnInfo(col_info)
            """
                    self.col_info['varnameTypes']= self.colname
                    self.col_info['defaultNumchar']= self.numchar_val
                    self.col_info['defaultInterval'] = self.default_interval
                    self.col_info['defaultNature'] = self.nature
                    self.col_info['defaultBinary'] = self.binary
                    self.col_info['defaultTime'] = self.time_val
            """
            # print(self.col_info)
            self.variable_dict[colname] = col_info
            # print(variable_dict)
            continue  # go to next variable


            #print(colname)
        # print()
        for key, val in self.variable_dict.items():
            print('col: %s' % key)
            print(json.dumps(val.as_dict(), indent=4))
        print('-- end of typeguess --')

    @staticmethod
    def is_number(s):
        """To check if the given number is numeric that is : digit, decimal or number"""

        try:
            float(s)
            return True
        except ValueError:
            pass
        try:
            int(s)
            return True
        except ValueError:
            pass

        try:
            import unicodedata
            unicodedata.numeric(s)
            return True
        except (TypeError, ValueError):
            pass


        return False

    @staticmethod
    def is_not_numeric(var_series):
        """Check if pandas Series is a numeric"""
        var_series.dropna(inplace=True)
        if(len(var_series)==0) or var_series.dtype=='bool':
            return True

        total = len(var_series)

        total_cnt = 0
        for val, cnt in var_series.value_counts().iteritems():

            if (TypeGuessUtil.is_number(val)):
                total_cnt=total_cnt+cnt

        if (total_cnt == total):

            print("THis is numeric")
            return False

        else:
            return True

    @staticmethod
    def is_logical(var_series):
        """Check if pandas Series is a boolean"""
        var_series.dropna(inplace=True)
        if(var_series.dtype=='bool'):
            #print("this is boolean")
            return True
        elif(var_series.dtype=='object'):

            total = len(var_series)
            total_cnt = 0
            for val, cnt in var_series.value_counts().iteritems():
                if (val == True or val == False):
                    total_cnt = total_cnt + cnt

            if (total_cnt == total):
                #print("this is boolean")
                return True

        return False

    def check_decimal(self,x):
        """Check if variable is a decimal"""
        result = False
        level = np.floor(x)
        if any(x != level):
            result = True

        return result

    def check_nature(self,x, c):
        if c:
            if 0 <= x <= 1:
                return NATURE_PERCENT
            elif 0 <= x <= 100 and min(x) < 15 and max(x) > 85:
                return NATURE_PERCENT
            else:
                return NATURE_RATIO

        else:
            return NATURE_ORDINAL

    def check_time(self,data_info):
        return "no"
