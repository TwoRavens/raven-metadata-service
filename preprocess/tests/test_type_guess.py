"""Unit testing module for Type guess"""
import unittest

from os.path import abspath, dirname, join, normpath, isdir, isfile
from io import StringIO
import json
import sys
import pandas as pd
import numpy as np

from msg_util import *
from type_guess_util import TypeGuessUtil
from col_info_constants import *


PREPROCESS_DIR = dirname(dirname(abspath(__file__)))
INPUT_DIR = join(PREPROCESS_DIR, 'input')
# add the 'code' directory to the sys path
sys.path.append(join(PREPROCESS_DIR, 'code'))


class TestTypeGuess(unittest.TestCase):
    """Unit testing class for type_guess_util"""
    def test_10_is_logical(self):
        """(10) Test the is_logical with logical Series"""
        msgt(self.test_10_is_logical.__doc__)

        msg('Test a logical series')
        series = pd.Series([True, False, True, True])
        self.assertTrue(TypeGuessUtil.is_logical(series))

        msg('Test a logical series that includes Nan and None')
        series = pd.Series([True, False, True, True, np.nan, None])
        self.assertTrue(TypeGuessUtil.is_logical(series))

    def test_20_is_logical_empty_string(self):
        """(20) Test series with empty string, expect not logical"""
        msgt(self.test_20_is_logical_empty_string.__doc__)

        series = pd.Series([True, False, True, True, ""])

        self.assertTrue(TypeGuessUtil.is_logical(series) is False)

    def test_30_is_logical_empty_list(self):
        """(30) Test empty series, expect not logical"""
        msgt(self.test_30_is_logical_empty_list.__doc__)

        series = pd.Series([])

        self.assertTrue(TypeGuessUtil.is_logical(series) is False)

    def test_40_series_with_string_booleans(self):
        """(40) Test series with 'TRUE', 'FALSE'"""
        msgt(self.test_40_series_with_string_booleans.__doc__)

        test_data = StringIO(('col1\n'
                              'TRUE\n'
                              'FALSE\n'
                              'TRUE\n'
                              'FALSE'))

        data_frame = pd.read_csv(test_data)
        series = data_frame['col1']

        self.assertTrue(TypeGuessUtil.is_logical(series))

        test_data = StringIO(('col1\n'
                              'TRUE\n'
                              '\n'
                              'FALSE\n'
                              'TRUE\n'
                              'FALSE'))

        data_frame = pd.read_csv(test_data)
        series = data_frame['col1']

        self.assertTrue(TypeGuessUtil.is_logical(series))

    def test_50_series_with_string_not_boolean(self):
        """(50) Test series with string 'Red', 'Blue'"""
        msgt(self.test_50_series_with_string_not_boolean.__doc__)

        test_data = StringIO(('col1\n'
                              'Red\n'
                              'Blue\n'
                              'Green\n'
                              'Purple'))

        data_frame = pd.read_csv(test_data)
        series = data_frame['col1']

        self.assertTrue(TypeGuessUtil.is_logical(series) is False)

        test_data = StringIO(('col1\n'
                              'Red\n'
                              '\n'
                              'Blue\n'
                              'Green\n'
                              'Purple'))

        data_frame = pd.read_csv(test_data)
        series = data_frame['col1']

        self.assertTrue(TypeGuessUtil.is_logical(series) is False)

    """ Test cases for is_not_numeric function"""

    def test_60_is_not_numeric(self):
        """(60) Test series with int eg: 2, 4, 8'"""
        msgt(self.test_60_is_not_numeric.__doc__)
        msg('Test a int series')
        series = pd.Series([2, 6, 7, 3, 2, 65])
        self.assertFalse(TypeGuessUtil.is_not_numeric(series))

    def test_70_is_not_numeric(self):
        """(70) Test series with float eg: 2, 4, 8'"""
        msgt(self.test_70_is_not_numeric.__doc__)
        msg('Test a float series')
        series = pd.Series([2.5, 3.4, 7.00008, 3.2, 2.12, 65.57659])
        self.assertFalse(TypeGuessUtil.is_not_numeric(series))

    def test_80_is_not_numeric_nan_values(self):
        """(80) Test series with nan eg: 2, 4, 8, NAN'"""
        msgt(self.test_80_is_not_numeric_nan_values.__doc__)
        msg('Test a numeric series with NAN')
        series = pd.Series([2.5, 3.4, 7.00008, np.nan, 2.12, 65.57659])
        self.assertFalse(TypeGuessUtil.is_not_numeric(series))

    def test_90_is_not_numeric_all_nan_values(self):
        """(90) Test series with nan eg: NAN,NAN, NAN'"""
        msgt(self.test_90_is_not_numeric_all_nan_values.__doc__)
        msg('Test a numeric series with all NAN')
        msg('Should be sent as a character i.e return True')
        series = pd.Series([np.nan, np.nan, np.nan])
        self.assertFalse(TypeGuessUtil.is_not_numeric(series) is False)

    def test_100_is_not_numeric_empty_strings(self):
        """(100) Test series with nan eg: 2,3.0,"",5'"""
        msgt(self.test_100_is_not_numeric_empty_strings.__doc__)
        msg('Test a numeric series with empty strings')
        msg('Should be sent as a character i.e return True')

        series = pd.Series([3, 4.9, "", 23])
        self.assertFalse(TypeGuessUtil.is_not_numeric(series) is False)

    def test_110_is_not_numeric_all_characters(self):
        """(110) Test series with string eg: 'price','Red'"""
        msgt(self.test_110_is_not_numeric_all_characters.__doc__)
        msg('Test a numeric series with strings')
        msg('Should be sent as a character i.e return True')

        series = pd.Series(['Red', 'Blue'])
        self.assertTrue(TypeGuessUtil.is_not_numeric(series))

    def test_120_is_not_numeric_boolean(self):
        """(120) Test the is_not_numeric with logical Series"""
        msgt(self.test_120_is_not_numeric_boolean.__doc__)

        msg('Test with a logical series')
        series = pd.Series([True, False, True, True])
        self.assertTrue(TypeGuessUtil.is_not_numeric(series))

    def test_130_is_not_numeric_boolean_nan(self):
        """(130) Test the is_not_numeric with nan"""
        msgt(self.test_130_is_not_numeric_boolean_nan.__doc__)

        msg('Test with a logical series with nan')
        series = pd.Series([True, False, np.nan, True, True, np.nan, False])
        self.assertTrue(TypeGuessUtil.is_not_numeric(series))

    def test_140_is_logical_all_nan(self):
        """(140) Test the is_logical with nan"""
        msgt(self.test_140_is_logical_all_nan.__doc__)

        msg('Test a logical series with nan')
        series = pd.Series([np.nan, np.nan, np.nan])
        self.assertFalse(TypeGuessUtil.is_logical(series))

    def test_150_nature_check_condition_1(self):
        """(150) Test the nature check condition 1 : if series(continuous) is between 0 and 1"""
        msgt(self.test_150_nature_check_condition_1.__doc__)
        msg('Test a (0,1) series')
        series = pd.Series([0.2, 0.6, 0.7, 0.3, 0.3, 1])
        self.assertEqual(TypeGuessUtil.check_nature(series, True), NATURE_PERCENT)

    def test_160_nature_check_condition_2(self):
        """(160) check condition 2 : if series(continuous) is between 0 and 100 and min < 15 and max > 85"""
        msgt(self.test_160_nature_check_condition_2.__doc__)
        msg('Test a int (0,100) series')
        series = pd.Series([1, 23, 12, 34, 99])
        self.assertEqual(TypeGuessUtil.check_nature(series, True), NATURE_PERCENT)

    def test_170_nature_check_condition_3(self):
        """(170) check condition 3 : if series(continuous) is between not  0 and 100 and min !< 15 and max !> 85"""
        msgt(self.test_170_nature_check_condition_3.__doc__)
        msg('Test a int any series')
        series = pd.Series([0.1, 223, 12, 34, 99])
        self.assertEqual(TypeGuessUtil.check_nature(series, True), NATURE_RATIO)

    def test_180_nature_check_condition_4(self):
        """(180) check condition 4 : if series(continuous) is between not  0 and 100 and min !< 15 and max !> 85"""
        msgt(self.test_180_nature_check_condition_4.__doc__)
        msg('Test a int discreet series')
        series = pd.Series([0.1, 223, 12, 34, 99, None])
        self.assertEqual(TypeGuessUtil.check_nature(series, False), NATURE_ORDINAL)

    def setUp(self):
        """Load up the test file"""
        self.df_01 = pd.DataFrame.from_csv(join(INPUT_DIR, 'test_file_01.csv'))
        type_guess_obj = TypeGuessUtil(self.df_01)
        self.variable_info_01 = type_guess_obj.get_variable_dict()

    def test_190_valid_check(self):
        """(10) Test the data for numeric series"""
        msgt(self.test_190_valid_check.__doc__)

        # Pull the ColumnInfo for Ranking
        col_info = self.variable_info_01.get('UN')

        # Calculate the stats
        TypeGuessUtil(self.df_01)
        dashes()
        # Check valid and invalid data
        msg('Check valid and invalid ')
        self.assertEqual(col_info.valid, 8)
        self.assertEqual(col_info.invalid, 3)

if __name__ == '__main__':
    unittest.main()
