import pandas as pd
import numpy as np
from pandas.api.types import *


class PreprocessUtils(object):

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
    def herfindahl_index(col_data, char, sum_val, drop_missing=True):
        # check again with the logic of calculating, what values are squared
        """Calculate Herfindahl-Hirschman Index (HHI) for the column data.
        For each given day, HHI is defined as a sum of squared weights of
        %values in a col_series; and varies from 1/N to 1.
        """
        fraction_val = []
        total_sum = 0
        if drop_missing:
            # redundant if not used as a staticmethod,
            # already happens at calc_stats init
            col_data.dropna(inplace=True)
        if char:
            total_sum = sum_val
            for val, val_cnt in col_data.value_counts().iteritems():
                fraction_val.append(np.math.pow(val_cnt / total_sum, 2))
        else:
            total_sum = sum(col_data)

            for val, cnt in col_data.items():
                fraction_val.append(np.math.pow(cnt / total_sum, 2))

        return sum(fraction_val)

    @staticmethod
    def ecdf_y_vlaue(x_cdf_val, raw_data):
        """Compute ECDF for a one-dimensional array of measurements"""

        size_data = raw_data.size
        # y-data for the ECDF: y
        y_value = []

        for i in x_cdf_val:
            temp = raw_data[raw_data <= i]
            val = temp.size / size_data
            y_value.append(val)

        return y_value

    @staticmethod
    def ecdf_x_vlaue(series, size):
        """Compute ECDF for a one-dimensional array of measurements."""
        # Number of data points: size

        val = np.linspace(start=min(series), stop=max(series), num=size)

        return val
