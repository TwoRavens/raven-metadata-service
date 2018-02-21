"""Unit testing for cal_stats_util using sample data"""
import unittest
from os.path import abspath, dirname, join
import pandas as pd

PREPROCESS_DIR = dirname(dirname(dirname(abspath(__file__))))
INPUT_DIR = join(PREPROCESS_DIR, 'input')

from msg_util import dashes, msgt, msg
from type_guess_util import TypeGuessUtil
from cal_stats_util import CalSumStatsUtil


class CalSumStatsTest(unittest.TestCase):
    """Unit testing class for cal_stats_util"""

    def setUp(self):
        """Load up the test file"""
        self.df_01 = pd.DataFrame.from_csv(join(INPUT_DIR, 'test_file_01.csv'))
        type_guess_obj = TypeGuessUtil(self.df_01)
        self.variable_info_01 = type_guess_obj.get_variable_dict()

    def test_10_numeric_val_ok(self):
        """(10) Test the data for numeric series"""
        msgt(self.test_10_numeric_val_ok.__doc__)

        # Pull the ColumnInfo for Ranking
        col_info = self.variable_info_01.get('quat')
        col_series = self.df_01[col_info.colname]

        # Calculate the stats
        CalSumStatsUtil(col_series, col_info)

        col_info.print_values()
        dashes()

        # Check uniques
        msg('Check uniques')
        self.assertEqual(col_info.uniques, 10)

        # Check valid and invalid data
        msg('Check valid and invalid ')
        self.assertEqual(col_info.valid, 12)
        self.assertEqual(col_info.invalid, 0)

        # Check median, mean, sd
        msg('Check median, mean, and sd')
        self.assertEqual(col_info.median, 2445)
        self.assertEqual(col_info.mean, 6692.272727272727)
        self.assertEqual(col_info.std_dev, 10148.778666331324)

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

    def test_20_non_numeric_val_ok(self):
        """(20) Test the data for non numeric series"""
        msgt(self.test_20_non_numeric_val_ok.__doc__)

        # Pull the ColumnInfo for Ranking
        col_info = self.variable_info_01.get('UN')
        col_series = self.df_01[col_info.colname]

        # Calculate the stats
        CalSumStatsUtil(col_series, col_info)

        col_info.print_values()
        dashes()

        # Check uniques
        msg('Check uniques')
        self.assertEqual(col_info.uniques, 2)

        # Check median, mean, sd
        msg('Check median, mean, and sd')
        self.assertEqual(col_info.median, "NA")
        self.assertEqual(col_info.mean, "NA")
        self.assertEqual(col_info.std_dev, "NA")

        # Check min, max
        msg('Check min, max')
        self.assertEqual(col_info.min, "NA")
        self.assertEqual(col_info.max, "NA")

        msg('Check mode, fewest, mid, etc')
        # Check mode, fewest, mid, etc
        self.assertEqual(col_info.mode, [True])
        self.assertEqual(col_info.freqmode, 5)
        self.assertEqual(col_info.mid, True)
        self.assertEqual(col_info.freqmid, 4)
        # Fewest and freqfewest discussion about the concept

        msg('Check herfindahl ')
        # Check herfindahl
        self.assertEqual(col_info.herfindahl, 0.53125)


if __name__ == '__main__':
    unittest.main()
