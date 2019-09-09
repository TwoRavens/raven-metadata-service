""" Module for type guessing """
import datetime

import pandas as pd
from pandas.api.types import is_float_dtype, is_numeric_dtype

import raven_preprocess.col_info_constants as col_const
from raven_preprocess.column_info import ColumnInfo
from raven_preprocess.basic_utils.basic_err_check import BasicErrCheck

date_fmts = [
    '%x', # 11/3/98
    '%Y-%m-%d', # 1958-01-08
    '%d %b %Y %H:%m', # 17 May 2014 09:38
]

class TypeGuessUtil(BasicErrCheck):
    """Check variable types of a dataframe"""
    def __init__(self, col_series, col_info):
        """Init with a pandas dataframe"""
        assert col_series is not None, "dataframe can't be None"

        self.col_series = col_series
        self.col_info = col_info
        self.col_info.time_val = col_const.UNKNOWN
        self.binary = False

        # final outout returned
        self.check_types()

    def check_types(self):
        """check the types of the dataframe"""
        # assert self.colnames, 'self.colnames must have values'

        self.col_info.invalid = int(self.col_series.isnull().sum())
        self.col_info.valid = int(self.col_series.count())

        # Drop nulls...
        self.col_series.dropna(inplace=True)

        self.col_info.binary = col_const.BINARY_YES if len(self.col_series.unique()) == 2 else col_const.BINARY_NO

        if self.is_not_numeric(self.col_series) or self.is_logical(self.col_series):
            fmt = self.check_time(self.col_series)
            if fmt:
                self.col_info.time_val = fmt 

            self.col_info.numchar_val = col_const.NUMCHAR_CHARACTER
            self.col_info.default_interval = col_const.INTERVAL_DISCRETE
            self.col_info.nature = col_const.NATURE_NOMINAL
        else:
            try:
                series_info = self.col_series.astype('int')
            except ValueError as e:
                self.add_err_msg('Type guess error when converting to int: %s' % e)
                return

            if any(series_info.isnull()):
                # CANNOT REACH HERE B/C NULLS ARE DROPPED!
                 
                self.col_info.numchar_val = col_const.NUMCHAR_CHARACTER
                self.col_info.nature = col_const.NATURE_NOMINAL
                self.col_info.default_interval = col_const.INTERVAL_DISCRETE
            else:
                self.col_info.numchar_val = col_const.NUMCHAR_NUMERIC

                ints = self.col_series.where(lambda x: x is 0 or x % 1 == 0.0)
                if is_float_dtype(self.col_series) and ints.count() != len(self.col_series):
                    self.col_info.default_interval = col_const.INTERVAL_CONTINUOUS
                    self.col_info.nature = self.check_nature(self.col_series, True)
                else:
                    self.col_info.default_interval = col_const.INTERVAL_DISCRETE
                    self.col_info.nature = self.check_nature(series_info, False)

    @staticmethod
    def is_not_numeric(var_series):
        """Check if pandas Series is a numeric"""
        assert isinstance(var_series, pd.Series), \
            "var_series must be a pandas.Series. Found type: (%s)" % type(var_series)

        if var_series.size == 0 or var_series.dtype == 'bool':
            return True

        return not is_numeric_dtype(var_series)

    @staticmethod
    def is_logical(var_series):
        """Check if pandas Series contains boolean values"""
        assert isinstance(var_series, pd.Series), \
            "var_series must be a pandas.Series. Found type: (%s)" % type(var_series)

        # Check the dtype
        #    "bool" - True, clearly logical
        #    "object" - possibly logical that had contained np.Nan
        #    ~anything else~ - False
        if var_series.dtype == 'bool':
            return True
        elif var_series.dtype != 'object':
            return False

        # It's an object.  Check if all the value seither True or False
        total = var_series.size
        total_cnt = 0
        for val, cnt in var_series.value_counts().iteritems():
            if val is True or val is False:
                total_cnt = total_cnt + cnt

        if total_cnt == total:
            # This is a boolean -- everything was either True or False
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
            return col_const.NATURE_RATIO
        return col_const.NATURE_ORDINAL

    @staticmethod
    def check_time(var_series):
        """Unimplemented"""
        assert isinstance(var_series, pd.Series), \
            "var_series must be a pandas.Series. Found type: (%s)" % type(var_series)

        if var_series.dtype == 'object':
            for fmt in date_fmts:
                try:
                    var_series[:10].str.strip().apply(lambda x: datetime.datetime.strptime(x, fmt))
                    return fmt
                except:
                    pass  
