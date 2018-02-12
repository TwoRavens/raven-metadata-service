import unittest

import json
import sys
from collections import OrderedDict
from os.path import abspath, dirname, join, normpath, isdir, isfile
import pandas as pd
import numpy as np
from io import StringIO

PREPROCESS_DIR = dirname(dirname(abspath(__file__)))
INPUT_DIR = join(PREPROCESS_DIR, 'input')
# add the 'code' directory to the sys path
sys.path.append(join(PREPROCESS_DIR, 'code'))

from msg_util import dashes, msgt, msg
from type_guess_util import TypeGuessUtil
from cal_stats_util import CalSumStatsUtil

class CalSumStatsTest(unittest.TestCase):

    def setUp(self):
        """Load up the test file"""
        self.df_01 = pd.DataFrame.from_csv(join(INPUT_DIR, 'test_file_01.csv'))
        type_guess_obj = TypeGuessUtil(self.df_01)
        self.variable_info_01 = type_guess_obj.get_variable_dict()


    def test_10_freq_ok(self):
        """(10) Test the frequency counts"""
        msgt(self.test_10_freq_ok.__doc__)

        # Pull the ColumnInfo for Ranking
        col_info = self.variable_info_01.get('quat')

        # Calculate the stats
        CalSumStatsUtil(self.df_01, col_info)

        col_info.print_values()
        dashes()

        # Check uniques
        msg('Check uniques')
        self.assertEqual(col_info.uniques, 10)

        # Check valid and invalid data
        msg('Check valid and invalid ')
        self.assertEqual(col_info.valid, 11)
        self.assertEqual(col_info.invalid, 0)

        # Check median, mean, sd
        msg('Check median, mean, and sd')
        self.assertEqual(col_info.median, 2445)
        self.assertEqual(col_info.mean, 6692.272727272727)
        self.assertEqual(col_info.sd,  10148.778666331324)




        # Check min, max
        msg('Check min, max')
        self.assertEqual(col_info.min, 12)
        self.assertEqual(col_info.max, 34314)

        msg('Check mode, fewest, mid, etc')
        # Check mode, fewest, mid, etc
        self.assertEqual(col_info.mode, 1232)
        self.assertEqual(col_info.freqmode, 2)
        self.assertEqual(col_info.mid, 1324)
        self.assertEqual(col_info.freqmid, 1)
        # Fewest and freqfewest discussion

        msg('Check herfindahl ')
        # Check herfindahl
        self.assertEqual(col_info.herfindahl, 0.2809709309217837)


if __name__ == '__main__':
    unittest.main()
