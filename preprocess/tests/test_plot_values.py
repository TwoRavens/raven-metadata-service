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
from plot_values import PlotValuesUtil


class PlotValuesTest(unittest.TestCase):
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
        PlotValuesUtil(self.df_01, col_info)

        col_info.print_values()
        dashes()

        # Check plottype, cdf plot type
        msg('Check Plot types')
        self.assertEqual(col_info.plot_type, 'bar')
        msg('Check Cdf Plot types')
        self.assertEqual(col_info.cdf_plottype, 'bar')