from collections import OrderedDict
from os.path import abspath, dirname, join
import sys

PREPROCESS_DIR = dirname(dirname(dirname(abspath(__file__))))
INPUT_DIR = join(PREPROCESS_DIR, 'input')

sys.path.append(PREPROCESS_DIR)

import pandas as pd
from raven_preprocess.summary_stats_util import SummaryStatsUtil
from raven_preprocess.column_info import ColumnInfo

def testit():
    print('testit')
    col_info = ColumnInfo('quat')
    df_01 = pd.read_csv(join(INPUT_DIR, 'test_file_01.csv'))

    ssu = SummaryStatsUtil((df_01['quat']), col_info)
    print(ssu.col_info.mid)

if __name__ == '__main__':
    testit()