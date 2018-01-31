import json
import sys
from collections import OrderedDict
from os.path import abspath, dirname, join, normpath, isdir, isfile

CURRENT_DIR = dirname(abspath(__file__))
INPUT_DIR = join(dirname(CURRENT_DIR), 'input')

import numpy as np
import pandas as pd


from type_guess_util import *
from cal_stats_util import CalSumStatsUtil
from column_info import *


class MyEncoder(json.JSONEncoder):
    def default(self, obj):

        if isinstance(obj, numpy.integer):
            return int(obj)
        elif isinstance(obj, numpy.floating):
            return float(obj)
        elif isinstance(obj, numpy.ndarray):
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

        calsumstats = CalSumStatsUtil(df, col_info)

    for col_name, col_info in variable_dict.items():
        col_info.print_values()

    
if __name__ == '__main__':
    input_file = join(INPUT_DIR, 'learningData.csv')
    test_run(input_file)



#To do list for preprocess.R -> preprocess.py
#1.Input from different sources
#2.function typeGuess()
#3.
