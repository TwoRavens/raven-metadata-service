"""Main module to call all sub modules"""
from __future__ import print_function
from collections import OrderedDict
from os.path import abspath, dirname, join, normpath, isdir, isfile
import json
import numpy as np
import pandas as pd

from preprocess_runner import PreprocessRunner

from type_guess_util import *
from cal_stats_util import CalSumStatsUtil
from column_info import *
from plot_values import *

CURRENT_DIR = dirname(abspath(__file__))
INPUT_DIR = join(dirname(CURRENT_DIR), 'input')
OUTPUT_DIR = join(dirname(CURRENT_DIR), 'output')


class MyEncoder(json.JSONEncoder):
    """class to encode the data"""
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
    """Main test run class for this module"""

    runner, err_msg = PreprocessRunner.load_from_csv_file(input_file)
    if err_msg:
        print(err_msg)
        return

    if runner.has_error:
        print(runner.error_message)
        return

    runner.show_final_info()

    jstring = runner.get_final_json(indent=4)
    print(jstring)

    return
    assert isfile(input_file), 'file not found: %s' % input_file

    # read file into dataframe
    data_frame = pd.read_csv(input_file)

    # use typeguess to produce variable_ifo which is a dict of ColumnInfo
    type_guess_util = TypeGuessUtil(data_frame)

    variable_dict = type_guess_util.get_variable_dict()
    # Iterate through variable info and
    # run calc stats on each ColumnInfo object
    #
    for col_name, col_info in variable_dict.items():
        # set stats for each column
        CalSumStatsUtil(data_frame, col_info)

    for col_name, col_info in variable_dict.items():
        # set stats for each column
        PlotValuesUtil(data_frame, col_info)

    # print results to screen--format variable section..
    fmt_variable_info = OrderedDict()
    for col_name, col_info in variable_dict.items():
        col_info.print_values()
        fmt_variable_info[col_name] = col_info.as_dict()

    overall_dict = OrderedDict()
    overall_dict['variables'] = fmt_variable_info
    variable_string = json.dumps(overall_dict, indent=4, cls=MyEncoder)
    print(variable_string)
    file_name = join(OUTPUT_DIR, 'variable_output_testfile1.json')
    open(file_name, 'w').write(variable_string)
    print('file written: %s' % file_name)

if __name__ == '__main__':
    INPUT_FILE = join(INPUT_DIR, 'test_file_01.csv')
    test_run(INPUT_FILE)
