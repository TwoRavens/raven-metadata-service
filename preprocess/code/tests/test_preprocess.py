"""Unit testing for summary_stats_util using sample data"""
import unittest
from unittest import skip
from os.path import abspath, dirname, isfile, join
import json
import decimal
from collections import OrderedDict
import col_info_constants as col_const
import update_constants as update_const
from preprocess_runner import PreprocessRunner

TEST_DATA_DIR = join(dirname(abspath(__file__)), 'test_data')
#INPUT_DIR = join(PREPROCESS_DIR, 'input')

from msg_util import dashes, msgt, msg
from variable_display_util import VariableDisplayUtil


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
        runner, err = PreprocessRunner.load_from_csv_file(basic_csv)


        self.assertTrue(err is None)
        self.assertTrue(runner.has_error is False)

        result_dict = runner.get_final_dict()

        print('result_dict', result_dict)

        self.assertEqual(result_dict['dataset']['row_cnt'], 4)
        self.assertEqual(result_dict['dataset']['variable_cnt'], 3)
