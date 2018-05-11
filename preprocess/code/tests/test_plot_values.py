""" Unit testing Module for plot values eg: type, cdf, labl etc"""
import unittest
from os.path import abspath, dirname, join
import pandas as pd

PREPROCESS_DIR = dirname(dirname(dirname(abspath(__file__))))
INPUT_DIR = join(PREPROCESS_DIR, 'input')

from msg_util import dashes, msgt, msg
from type_guess_util import TypeGuessUtil
from plot_values import PlotValuesUtil
from column_info import ColumnInfo
from summary_stats_util import SummaryStatsUtil
class PlotValuesTest(unittest.TestCase):
    """ class to test Module for plot values eg: type, cdf, labl etc"""

    def setUp(self):
        """Load up the test file"""
        self.df_01 = pd.DataFrame.from_csv(join(INPUT_DIR, 'test_file_01.csv'))
        self.col_info = ColumnInfo('quat')
        TypeGuessUtil(self.df_01['quat'],self.col_info)
        SummaryStatsUtil((self.df_01['quat']), self.col_info)
        PlotValuesUtil(self.df_01['quat'], self.col_info)

    def test_10_plot_values_ok(self):
        """(10) Test plot values of column"""
        msgt(self.test_10_plot_values_ok.__doc__)

        # Pull the ColumnInfo for Ranking
        col_info = self.col_info
        # Calculate the stats


        col_info.print_values()
        dashes()

        # Check plottype, cdf plot type
        msg('Check Plot types')
        self.assertEqual(col_info.plot_type, 'bar')
        msg('Check Cdf Plot types')
        self.assertEqual(col_info.cdf_plot_type, 'bar')

        # Check cdf plot values
        cdfx = pd.DataFrame([12.0,
                3823.3333333333335,
                7634.666666666667,
                11446.0,
                15257.333333333334,
                19068.666666666668,
                22880.0,
                26691.333333333336,
                30502.666666666668,
                34314.0])
        cdfy = pd.DataFrame([0.08333333333333333,
                0.5833333333333334,
                0.6666666666666666,
                0.75,
                0.9166666666666666,
                0.9166666666666666,
                0.9166666666666666,
                0.9166666666666666,
                0.9166666666666666,
                1.0])

        msg('Check cdf plot values')
        print("cdfx", col_info.cdf_plotx)
        self.assertTrue(pd.DataFrame(col_info.cdf_plotx).equals(cdfx))
        self.assertTrue(pd.DataFrame(col_info.cdf_ploty).equals(cdfy))


if __name__ == '__main__':
    unittest.main()
