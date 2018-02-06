import unittest

import json
import sys
from collections import OrderedDict
from os.path import abspath, dirname, join, normpath, isdir, isfile
import pandas as pd
import numpy as np
from io import StringIO

PREPROCESS_DIR = dirname(dirname(abspath(__file__)))
# add the 'code' directory to the sys path
sys.path.append(join(PREPROCESS_DIR, 'code'))

from msg_util import *
from type_guess_util import TypeGuessUtil

class TestTypeGuess(unittest.TestCase):

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

        df = pd.read_csv(test_data)
        series = df['col1']

        self.assertTrue(TypeGuessUtil.is_logical(series))

        test_data = StringIO(('col1\n'
                              'TRUE\n'
                              '\n'
                              'FALSE\n'
                              'TRUE\n'
                              'FALSE'))

        df = pd.read_csv(test_data)
        series = df['col1']

        self.assertTrue(TypeGuessUtil.is_logical(series))


if __name__ == '__main__':
    unittest.main()
