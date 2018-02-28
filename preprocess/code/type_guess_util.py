""" Module for type guessing """
import pandas as pd
from pandas.api.types import is_float_dtype, is_numeric_dtype

import col_info_constants as col_const
from column_info import ColumnInfo


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
        self.binary = False
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

            # retrieve the Series from the DataFrame
            #
            series_info = self.dataframe[colname]

            # number of missing entries
            #
            col_info.invalid = int(series_info.isnull().sum())

            # number of valid entries
            #
            col_info.valid = int(series_info.count())

            # set time , what exactly we want to do with this
            #
            col_info.time_val = self.check_time(series_info)

            # Drop nulls...
            series_info.dropna(inplace=True)

            uniques = series_info.unique()

            binary = self.check_binary(len(uniques))

            # set up binary values..
            if binary:
                col_info.binary = col_const.BINARY_YES
            else:
                col_info.binary = col_const.BINARY_NO

            if self.is_not_numeric(series_info) or self.is_logical(series_info):

                col_info.numchar_val = col_const.NUMCHAR_CHARACTER
                col_info.default_interval = col_const.INTERVAL_DISCRETE
                col_info.nature = col_const.NATURE_NOMINAL
                self.variable_dict[colname] = col_info

                continue    # go onto next column

            series_info = series_info.astype('int')

            if any(series_info.isnull()):
                # CANNOT REACH HERE B/C NULLS ARE DROPPED!
                #
                col_info.numchar_val = col_const.NUMCHAR_CHARACTER
                col_info.nature = col_const.NATURE_NOMINAL
                col_info.default_interval = col_const.INTERVAL_DISCRETE
            else:
                col_info.numchar_val = col_const.NUMCHAR_NUMERIC

                if is_float_dtype(series_info):
                    col_info.default_interval = col_const.INTERVAL_CONTINUOUS
                    col_info.nature = self.check_nature(series_info, True)

                else:
                    col_info.default_interval = col_const.INTERVAL_DISCRETE
                    col_info.nature = self.check_nature(series_info, False)

            self.variable_dict[colname] = col_info

    @staticmethod
    def is_not_numeric(var_series):
        """Check if pandas Series is a numeric"""
        assert isinstance(var_series, pd.Series), \
            "var_series must be a pandas.Series. Found type: (%s)" % type(var_series)

        var_series.dropna(inplace=True)
        if var_series.size == 0:
            # print("character")
            return True
        elif var_series.dtype == 'bool':
            return True

        if is_numeric_dtype(var_series):
            return False
        else:
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
    def check_nature(data_series, continuous_check):
        """Check the nature of the Series"""
        if continuous_check:
            if data_series.between(0, 1).all():
                return col_const.NATURE_PERCENT
            elif data_series.between(0, 100).all() and min(data_series) < 15 and max(data_series) > 85:
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

    @staticmethod
    def check_binary(unique_size):
        """ check if the series is binary or not """
        if unique_size is 2:
            return True
        else:
            return False
