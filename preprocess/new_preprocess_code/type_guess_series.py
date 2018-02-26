import pandas as pd
from pandas.api.types import *

import col_info_constants as col_const
from column_info import ColumnInfo
from preprocess_utilities import *


class TypeGuessSeries(object):
    """Check variable types of a Series"""
    def __init__(self, col_series):
        """Init with a pandas dataframe"""
        assert col_series is not None, "Series can't be None"

        self.col_series = col_series

        self.variable_dict = {}
        self.check_leaf()

    def check_leaf(self):
        # number of missing entries
        #
        col_info.invalid = int(self.col_series.isnull().sum())

        # number of valid entries
        #
        col_info.valid = int(self.col_series.count())

        if PreprocessUtils.is_logical() or PreprocessUtils.is_not_numeric():
            """classification for the discrete or continuous"""
