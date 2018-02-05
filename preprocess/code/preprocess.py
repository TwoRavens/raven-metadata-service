import json
import sys
from collections import OrderedDict
from os.path import abspath, dirname, join, normpath, isdir, isfile

CURRENT_DIR = dirname(abspath(__file__))
INPUT_DIR = join(dirname(CURRENT_DIR), 'input')
OUTPUT_DIR = join(dirname(CURRENT_DIR), 'output')

import numpy as np
import pandas as pd


from type_guess_util import *
from cal_stats_util import CalSumStatsUtil
from column_info import *


class MyEncoder(json.JSONEncoder):
    def default(self, obj):

        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        else:
            return super(MyEncoder, self).default(obj)

# if file input valid
def test_run(input_file):

    assert isfile(input_file), 'file not found: %s' % input_file

    # read file into dataframe
    df = pd.read_csv(input_file)

    # use typeguess to produce variable_ifo which is a dict of ColumnInfo
    type_guess_util = TypeGuessUtil(df)

    variable_dict = type_guess_util.get_variable_dict()
    var = OrderedDict()

    # Iterate through variable info and
    # run calc stats on each ColumnInfo object
    #
    for col_name, col_info in variable_dict.items():
        # set stats for each column
        calsumstats = CalSumStatsUtil(df, col_info)


    for col_name, col_info in variable_dict.items():
        # set stats for each column
        plotvalues = CalSumStatsUtil(df, col_info)

    # print results to screen--format variable section..
    fmt_variable_info = OrderedDict()
    for col_name, col_info in variable_dict.items():
        col_info.print_values()
        fmt_variable_info[col_name] = col_info.as_dict()

    overall_dict = OrderedDict()
    overall_dict['variables'] = fmt_variable_info
    variable_string = json.dumps(overall_dict, indent=4, cls=MyEncoder)
    print(variable_string)
    fname = join(OUTPUT_DIR, 'variable_output_titanic.json')
    open(fname, 'w').write(variable_string)
    print('file written: %s' % fname)

if __name__ == '__main__':
    input_file = join(INPUT_DIR, 'Testfile1.csv')
    test_run(input_file)



#To do list for preprocess.R -> preprocess.py
#1.Input from different sources
#2.function typeGuess()
#3.
