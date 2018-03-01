"""Unit testing module for Type guess"""
import unittest

from os.path import abspath, dirname, join
from io import StringIO

import pandas as pd
import numpy as np
from msg_util import msg, msgt, dashes
from type_guess_series import *
import col_info_constants as col_const


PREPROCESS_DIR = dirname(dirname(dirname(abspath(__file__))))
INPUT_DIR = join(PREPROCESS_DIR, 'input')




class TestTypeGuess(unittest.TestCase):
    """Unit testing class for type_guess_util"""
    def test_10_is_logical(self):
        """(10) Test the is_logical with logical Series"""
        msgt(self.test_10_is_logical.__doc__)

        msg('Test a logical series')
        series = pd.Series([True, False, True, True])
        print(TypeGuessSeries(series, 'UN'))


if __name__ == '__main__':
    unittest.main()


