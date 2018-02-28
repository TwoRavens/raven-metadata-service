import pandas as pd
from pandas.api.types import *

import col_info_constants as col_const
from column_info import ColumnInfo
from preprocess_utilities import *


class TypeGuessSeries(object):
    """Check variable types of a Series"""
    def __init__(self, col_series, col_info):
        """Init with a pandas dataframe"""
        assert col_series is not None, "Series can't be None"

        self.col_series = col_series
        self.col_info = col_info
        self.variable_dict = {}
        self.purpose = []
        self.check_leaf()

    def check_leaf(self):
        # number of missing entries
        #
        col_const.invalid = int(self.col_series.isnull().sum())

        # number of valid entries
        #
        col_const.valid = int(self.col_series.count())

        self.col_series.dropna(inplace=True)
        uniques = self.col_series.unique()

        if is_float_dtype(self.col_series):
            """ These are classified as continuous and numeric"""
            # Can a String be continuous, No?
            # ratio, percent, time or other
            self.purpose.append(col_const.INTERVAL_CONTINUOUS)
            if PreprocessUtils.check_nature(self.col_series) == col_const.NATURE_PERCENT:
                self.purpose.append(col_const.NATURE_PERCENT)
                if self.col_series.between(0, 1).all():
                    self.purpose.append(col_const.PERCENT_01)
                elif self.col_series.between(0, 100).all():
                    self.purpose.append(col_const.PERCENT_100)
            elif PreprocessUtils.check_nature(self.col_series) == col_const.NATURE_RATIO:
                self.purpose.append(col_const.NATURE_RATIO)

            elif PreprocessUtils.check_time(self.col_series):
                self.purpose.append(col_const.TIME)

            else:
                self.purpose.append(col_const.NATURE_OTHER)

        else:
            """They are classified as discrete and numeric/character"""
            # clear definition required for ordinal and nominal
            self.purpose.append(col_const.INTERVAL_DISCRETE)
            # dichotomous, ordinal, nominal
            if 0 < len(uniques) <= 2:  # or any other condition
                """ discrete : dichotomous """
                # elif: check for dichotomous with other conditions also
                self.purpose.append(col_const.NATURE_DICHOTOMOUS)

                if PreprocessUtils.is_logical(self.col_series):
                    self.purpose.append(col_const.DICHOTOMOUS_LOGICAL)
                elif is_numeric_dtype(uniques) or len(uniques) == 2:
                    self.purpose.append(col_const.DICHOTOMOUS_BINARY)
                else:
                    self.purpose.append(col_const.DICHOTOMOUS_OTHER)  # may be other classification definition

            elif is_categorical_dtype(self.col_series):
                # is categorical best definition for nominal data
                """ classification : character or boolean"""
                self.purpose.append(col_const.NATURE_NOMINAL)

            else:
                """ discrete : numeric : ordinal"""
                self.purpose.append(col_const.NATURE_ORDINAL)
                if self.col_series.count() > 0:
                    self.purpose.append(col_const.ORDINAL_COUNT)
                # elif 'others'

        col_const.purpose = self.purpose
        print(self.purpose)






