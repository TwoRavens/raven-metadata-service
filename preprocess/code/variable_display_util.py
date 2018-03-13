""" Module for variable display setting """
import pandas as pd
from pandas.api.types import is_float_dtype, is_numeric_dtype

import col_info_constants as col_const
from column_info import ColumnInfo


class VariableDisplayUtil(object):
    def __init__(self, col_series, col_info):
        """Init with a pandas dataframe"""
        assert col_series is not None, "dataframe can't be None"

        self.col_series = col_series
        self.col_info = col_info
        self.binary = False
        # # final outout returned
        self.var_display()

    def var_display(self):
        self.col_info.viewalbe = True

