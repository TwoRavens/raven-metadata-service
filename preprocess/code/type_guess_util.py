import json
import numpy as np
import pandas as pd

import col_info_constants as col_const
from column_info import ColumnInfo
from pandas.api.types import *


class TypeGuessUtil(object):
    """Check variable types of a dataframe"""
    def __init__(self, dataframe):
        """Init with a pandas dataframe"""
        assert dataframe is not None, "dataframe can't be None"

        self.dataframe = dataframe
        self.colnames = self.dataframe.columns
        self.colcount = len(self.dataframe.columns)
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
        # assert self.colnames, 'self.colnames must have values'

        # Iterate though variables and set type info
        for colname in self.colnames:
            col_info = ColumnInfo(colname)
            data_info = self.dataframe[colname]
            col_info.invalid = int(data_info.isnull().sum())
            col_info.valid = int(data_info.count())
            # set time , what exactly we want to do with this
            col_info.time_val = self.check_time(data_info)

            if self.is_not_numeric(data_info) or self.is_logical(data_info):

                col_info.numchar_val = col_const.NUMCHAR_CHARACTER
                col_info.default_interval = col_const.INTERVAL_DISCRETE
                col_info.nature = col_const.NATURE_NOMINAL

                data_info.dropna(inplace=True)
                if len(data_info.unique()) == 2:
                    col_info.binary = col_const.BINARY_YES
                else:
                    col_info.binary = col_const.BINARY_NO

                self.variable_dict[colname] = col_info

                continue    # go onto next column

            # Drop nulls...
            data_info.dropna(inplace=True)

            data_info = data_info.astype('int')
            # print(data_info)

            if len(data_info.unique()) == 2:
                col_info.binary = col_const.BINARY_YES
            else:
                col_info.binary = col_const.BINARY_NO

            if any(data_info.isnull()):
                # DOES IT EVER REACH? AFTER earlier .dropna...
                col_info.numchar_val = col_const.NUMCHAR_CHARACTER
                col_info.nature = col_const.NATURE_NOMINAL
                col_info.default_interval = col_const.INTERVAL_DISCRETE
            else:
                col_info.numchar_val = col_const.NUMCHAR_NUMERIC

                if is_float_dtype(data_info):
                    col_info.default_interval = col_const.INTERVAL_CONTINUOUS
                    col_info.nature = self.check_nature(data_info, True)
                    # print("#5")
                    # print(col_info.nature)
                else:
                    col_info.default_interval = col_const.INTERVAL_DISCRETE
                    col_info.nature = self.check_nature(data_info, False)

            self.variable_dict[colname] = col_info
            # print(variable_dict)
            continue  # go to next variable

        # for key, val in self.variable_dict.items():
        #     print('col: %s' % key)
        #     print(json.dumps(val.as_dict(), indent=4))
        # print('-- end of typeguess --')

    @staticmethod
    def is_number(val):
        """To check if the given number is numeric that is : digit, decimal or number"""
        if not val:
            return False

        try:
            float(val)
            return True
        except ValueError:
            pass
        try:
            int(val)

            return True
        except ValueError:
            pass

        try:
            import unicodedata
            unicodedata.numeric(val)
            return True
        except (TypeError, ValueError):
            pass
        return False

    @staticmethod
    def is_not_numeric(var_series):
        """Check if pandas Series is a numeric"""
        assert isinstance(var_series, pd.Series), \
            "var_series must be a pandas.Series. Found type: (%s)" % type(var_series)

        var_series.dropna(inplace=True)
        if var_series.size == 0:
            # print("character")
            return True

        total = len(var_series)

        total_cnt = 0
        for val, cnt in var_series.value_counts().iteritems():
            # val can be bool whose numeric value is 0 or 1.
            if isinstance(val, bool):
                continue
            elif TypeGuessUtil.is_number(val):
                total_cnt += cnt

        if total_cnt == total:
            # print("This is numeric")
            return False

        # print("character")
        return True

    @staticmethod
    def is_logical(var_series):
        """Check if pandas Series contains boolean values"""
        assert isinstance(var_series, pd.Series), \
            "var_series must be a pandas.Series. Found type: (%s)" % type(var_series)

        var_series.dropna(inplace=True)

        # Check the dtype
        #    "bool" - True, clearly logical
        #    "object" - possibly logical that had contained np.Nan
        #    ~anything else~ - False
        #
        if var_series.dtype == 'bool':
            return True
        elif var_series.dtype != 'object':
            return False

        # It's an object.  Check if all the values
        #   either True or False
        #
        total = var_series.size
        total_cnt = 0
        for val, cnt in var_series.value_counts().iteritems():
            if val is True or val is False:
                total_cnt = total_cnt + cnt

        if total_cnt == total:
            # This is a boolean -- everything was either True or False
            #
            return True

        return False

    @staticmethod
    def check_nature(x, c):
        """Check the nature of the Series"""
        if c:
            if x.between(0, 1).all():
                return col_const.NATURE_PERCENT
            elif x.between(0, 100).all() and min(x) < 15 and max(x) > 85:
                return col_const.NATURE_PERCENT
            else:
                return col_const.NATURE_RATIO

        else:
            return col_const.NATURE_ORDINAL

    @staticmethod
    def check_time(var_series):
        """Unimplemented"""
        assert isinstance(var_series, pd.Series), \
            "var_series must be a pandas.Series. Found type: (%s)" % type(var_series)

        return col_const.NOT_IMPLEMENTED
