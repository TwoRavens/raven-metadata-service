from os.path import abspath, dirname, join, normpath, isdir, isfile
from io import StringIO
import json
import sys
import pandas as pd
import numpy as np


PREPROCESS_DIR = dirname(dirname(abspath(__file__)))
INPUT_DIR = join(PREPROCESS_DIR, 'input')
# add the 'code' directory to the sys path
sys.path.append(join(PREPROCESS_DIR, 'code'))

from msg_util import msg, msgt, dashes
from type_guess_util import TypeGuessUtil
import col_info_constants as col_const

def main():
    df = pd.DataFrame.from_csv(join(INPUT_DIR, 'test_file_01.csv'),
                               index_col=None)

    print(df.columns)
    #df.columns
    col = df['Id']

    col_oil = df['oil']
    print('isnull', col_oil.isnull())
    print('isnull', col_oil.isnull().sum(), int(col_oil.isnull().sum()))
    print('valid', col_oil.count())
    return
    #val_counts = col.value_counts(sort=False, ascending=False)

    pairs = []
    for col_val, val_cnt in col.value_counts(sort=True).iteritems():
        print(col_val, val_cnt)
        pairs.append((col_val, val_cnt))

    #print(sorted(pairs, key=lambda x_val: (x_val[1], x_val[0]), reverse=True))
    #import ipdb; ipdb.set_trace()

if __name__ == '__main__':
    main()
