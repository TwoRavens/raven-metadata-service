"""Unit testing for summary_stats_util using sample data"""
import unittest
from os.path import abspath, dirname, join
import json
from collections import OrderedDict

TEST_DATA_DIR = join(dirname(abspath(__file__)), 'test_data')
#INPUT_DIR = join(PREPROCESS_DIR, 'input')

from msg_util import dashes, msgt, msg
from variable_display_util import VariableDisplayUtil


class UpdatePreprocessTest(unittest.TestCase):
    """Unit testing class for summary_stats_util"""

    def setUp(self):
        """Load up the test file"""
        update_01_fname = join(TEST_DATA_DIR, 'update_01.json')
        preprocess_01_fname = join(TEST_DATA_DIR, 'preprocess_01.json')
        update_data = open(update_01_fname, 'r').read()
        preprocess_data = open(preprocess_01_fname, 'r').read()
        self.update_json_01 = json.loads(update_data,
                                         object_pairs_hook=OrderedDict)
        self.preprocess_json_01 = json.loads(preprocess_data,
                                             object_pairs_hook=OrderedDict)

    def test_10_update(self):
        """(10) Test the data for numeric series"""
        msgt(self.test_10_update.__doc__)
        print(self.update_json_01)
        print(self.preprocess_json_01)

        self.assertTrue('preprocess_id' in self.update_json_01)
        # self.assertTrue('preprocess_id' in self.preprocess_json_01)


    def test_20_update(self):
        """(20) Test the data for numeric series"""
        msgt(self.test_20_update.__doc__)
        var_display_util = VariableDisplayUtil(self.preprocess_json_01, self.update_data)
        if var_display_util.has_error:
            print (var_display_util.error_messages)
