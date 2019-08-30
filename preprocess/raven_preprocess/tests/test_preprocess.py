"""Unit testing for preprocess_runner using sample data"""
import unittest
from unittest import skip
from os.path import abspath, dirname, isfile, join
import json
import decimal
from collections import OrderedDict
import sys
from os.path import \
    (abspath, basename, dirname, isdir, isfile, join, splitext)


import raven_preprocess.col_info_constants as col_const
import raven_preprocess.update_constants as update_const
from raven_preprocess.preprocess_runner import PreprocessRunner
from raven_preprocess.data_source_info import SOURCE_TYPE_FILE
from raven_preprocess.file_format_constants import \
    (CSV_FILE_EXT, TAB_FILE_EXT, get_mime_type)
from raven_preprocess.msg_util import dashes, msgt, msg

TEST_DATA_DIR = join(dirname(abspath(__file__)), 'test_data')
# INPUT_DIR = join(PREPROCESS_DIR, 'input')



class PreprocessTest(unittest.TestCase):
    """Unit testing class for summary_stats_util"""

    def get_file_path(self, fname):
        """Return a file path from the test directory"""
        return join(TEST_DATA_DIR, fname)

    def get_file_content(self, fname, as_json_dict=True):

        full_filename = join(TEST_DATA_DIR, fname)
        assert isfile(full_filename),\
            'Set up file not found: %s' % full_filename

        content = open(full_filename, 'r').read()

        if not as_json_dict:
            return content

        return json.loads(content,
                          object_pairs_hook=OrderedDict,
                          parse_float=decimal.Decimal)

    def setUp(self):
        """Load up tests as OrderedDict objects--unless specified otherwise"""
        #self.expected_data_01 = self.get_file_content('expected_data_01.json')

        #self.update_json_01 = self.get_file_content('update_json_01.json')

        #self.test_csv_01 = self.get_file_content('editor_test.csv')


        #self.test_040_file = self.get_file_content(\
        #                            'test_040_preprocess_file.json')

        #self.test_050_input = self.get_file_content('test_050_input.json')

    #@skip('skipit')
    def test_010_basic_preprocess(self):
        """(10) Preprocess a file"""
        msgt(self.test_010_basic_preprocess.__doc__)

        basic_csv = self.get_file_path('editor_test.csv')
        run_info = PreprocessRunner.load_from_file(basic_csv, job_id=1)

        print('=' * 40)
        self.assertTrue(run_info.success is True)

        runner = run_info.result_obj

        result_dict = runner.get_final_dict()

        print('result_dict', result_dict)

        self.assertEqual(result_dict[col_const.DATASET_LEVEL_KEY][col_const.DATASET_ROW_CNT], 4)
        self.assertEqual(result_dict[col_const.DATASET_LEVEL_KEY][col_const.DATASET_VARIABLE_CNT], 3)

        self.assertEqual(\
            result_dict[col_const.DATASET_LEVEL_KEY][col_const.DATA_SOURCE_INFO][col_const.DATA_SOURCE_TYPE],
            SOURCE_TYPE_FILE)

        self.assertEqual(\
            result_dict[col_const.DATASET_LEVEL_KEY][col_const.DATA_SOURCE_INFO][col_const.DATA_SOURCE_FORMAT],
            get_mime_type(CSV_FILE_EXT))

        self.assertEqual(\
            result_dict[col_const.DATASET_LEVEL_KEY][col_const.DATA_SOURCE_INFO][col_const.DATA_SOURCE_NAME],
            'editor_test.csv')


    #@skip('skipit')
    def test_020_basic_preprocess(self):
        """(20) Preprocess a tab delimeter file"""
        msgt(self.test_020_basic_preprocess.__doc__)

        basic_tab = self.get_file_path('editor_test.tab')
        run_info = PreprocessRunner.load_from_file(basic_tab, job_id=1)

        self.assertTrue(run_info.success is True)

        runner = run_info.result_obj

        result_dict = runner.get_final_dict()

        print('result_dict', result_dict)

        self.assertEqual(result_dict[col_const.DATASET_LEVEL_KEY][col_const.DATASET_ROW_CNT], 4)
        self.assertEqual(result_dict[col_const.DATASET_LEVEL_KEY][col_const.DATASET_VARIABLE_CNT], 3)
        self.assertEqual(result_dict[col_const.DATASET_LEVEL_KEY][col_const.DATA_SOURCE_INFO][col_const.DATA_SOURCE_TYPE], SOURCE_TYPE_FILE)
        self.assertEqual(result_dict[col_const.DATASET_LEVEL_KEY][col_const.DATA_SOURCE_INFO][col_const.DATA_SOURCE_FORMAT], get_mime_type(TAB_FILE_EXT))
        self.assertEqual(result_dict[col_const.DATASET_LEVEL_KEY][col_const.DATA_SOURCE_INFO][col_const.DATA_SOURCE_NAME], 'editor_test.tab')


if __name__ == '__main__':
    unittest.main()
