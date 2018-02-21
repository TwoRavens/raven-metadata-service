""" Unit testing Module for plot values eg: type, cdf, labl etc"""
import unittest
from os.path import abspath, dirname, join
import pandas as pd

PREPROCESS_DIR = dirname(dirname(dirname(abspath(__file__))))
INPUT_DIR = join(PREPROCESS_DIR, 'input')

from msg_util import dashes, msgt, msg
from type_guess_util import TypeGuessUtil
from plot_values import PlotValuesUtil

class PlotValuesTest(unittest.TestCase):
    """ class to test Module for plot values eg: type, cdf, labl etc"""

    def setUp(self):
        """Load up the test file"""
        self.df_01 = pd.DataFrame.from_csv(join(INPUT_DIR, 'test_file_01.csv'))
        type_guess_obj = TypeGuessUtil(self.df_01)
        self.variable_info_01 = type_guess_obj.get_variable_dict()

    def test_10_plot_values_ok(self):
        """(10) Test plot values of column"""
        msgt(self.test_10_plot_values_ok.__doc__)

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

        # Check cdf plot values
        cdfx = pd.DataFrame([12, 3823.33333333333, 7634.66666666667, 11446, 15257.3333333333, 19068.6666666667, 22880,
                             26691.3333333333, 30502.6666666667, 34314])
        cdfy = pd.DataFrame([0.0909090909090909, 0.636363636363636, 0.727272727272727, 0.818181818181818, 0.909090909090909,
                             0.909090909090909, 0.909090909090909, 0.909090909090909, 0.909090909090909, 1])

        msg('Check cdf plot values')
        print("cdfx", col_info.cdf_plotx)
        self.assertTrue(pd.DataFrame(col_info.cdf_plotx).equals(cdfx))
        self.assertTrue(pd.DataFrame(col_info.cdf_ploty).equals(cdfy))


if __name__ == '__main__':
    unittest.main()