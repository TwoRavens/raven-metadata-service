"""Unit testing for summary_stats_util using sample data"""
import unittest
from os.path import abspath, dirname, isfile, join
import json
from collections import OrderedDict

TEST_DATA_DIR = join(dirname(abspath(__file__)), 'test_data')
#INPUT_DIR = join(PREPROCESS_DIR, 'input')

from msg_util import dashes, msgt, msg
from variable_display_util import VariableDisplayUtil


class UpdatePreprocessTest(unittest.TestCase):
    """Unit testing class for summary_stats_util"""

    def get_file_content(self, fname, as_json_dict=True):

        full_filename = join(TEST_DATA_DIR, fname)
        assert isfile(full_filename),\
            'Set up file not found: %s' % full_filename

        content = open(full_filename, 'r').read()

        if not as_json_dict:
            return content

        return json.loads(content,
                          object_pairs_hook=OrderedDict)

    def setUp(self):
        """Load up tests as OrderedDict objects--unless specified otherwise"""
        self.test_20_expected_data = self.get_file_content('test_20_expected_data.json')

        self.update_json_01 = self.get_file_content('update_org.json')

        self.test_input_01 = self.get_file_content('test_input_01.json')

        self.test_40_file = self.get_file_content(\
                                    'test_40_preprocess_file.json',
                                    as_json_dict=False)

        self.test_50_input = self.get_file_content('test_50_input.json')

    def test_10_update(self):
        """(10) Test the data for numeric series"""
        msgt(self.test_10_update.__doc__)

        self.assertTrue('preprocess_id' in self.update_json_01)
        # self.assertTrue('preprocess_id' in self.test_input_01)


    def test_20_update(self):
        """(20) Test output json"""
        msgt(self.test_20_update.__doc__)
        var_util = VariableDisplayUtil(self.test_input_01, self.update_json_01)

        success, var_display_util = True, var_util.get_updated_metadata()

        self.assertTrue(success)
        self.assertEqual(var_display_util, self.test_20_expected_data)


    def test_30_update(self):
        """(30) test if there is no error"""
        msgt(self.test_30_update.__doc__)
        var_display = VariableDisplayUtil(self.test_input_01,
                                          self.update_json_01)
        self.assertTrue(var_display)

    def test_40_update(self):
        """(40) test for variable section not found in preprocess file"""
        msgt(self.test_40_update.__doc__)
        pre_file = self.test_40_file

        var_display_modify = VariableDisplayUtil(pre_file, self.update_json_01)
        var_err = var_display_modify.error_messages
        self.assertTrue(var_display_modify.has_error)
        print("Error : ", var_err)

    def test_50_update(self):
        """(50) test for variable display section not found in preprocess file"""
        msgt(self.test_50_update.__doc__)

        var_display_modify = VariableDisplayUtil(self.test_50_input, self.update_json_01)
        var_err = var_display_modify.error_messages
        self.assertTrue(var_display_modify.has_error)

        print("Error : ", var_err)

    def test_60_update(self):
        """(60) test for variable display section not found in preprocess file"""
        msgt(self.test_60_update.__doc__)

        update = {"preprocess_id": 45}
        var_display_modify = VariableDisplayUtil(self.test_input_01, update)
        var_err = var_display_modify.error_messages
        self.assertTrue(var_display_modify.has_error)

        print("Error : ", var_err)

    def test_70_update(self):
        """(70) test for variable display section's viewable not found in update file"""
        msgt(self.test_70_update.__doc__)
        update = {
            "preprocess_id": 45,
            "variable_updates": {
               "cylinders" : {
                 "omit": ["mean", "median"],
                 "value_updates": {
                     "numchar": "discrete",
                     "nature": "ordinal"
                 }
               },
               "mpg": {
                 "viewable": "false",
                 "omit": [],
                 "value_updates": {
                 }
               }
            }
        }

        var_display_modify = VariableDisplayUtil(self.test_input_01, update)
        var_err = var_display_modify.error_messages
        self.assertTrue(var_display_modify.has_error)
        print("Error : ", var_err)

    def test_80_update(self):
        """(80) test for variable display section's omit not found in update file"""
        msgt(self.test_80_update.__doc__)
        update = {
            "preprocess_id": 45,
            "variable_updates": {
               "cylinders" : {
                   "viewable": "true",
                 "omit": ["mean", "median"],
                 "value_updates": {
                     "numchar": "discrete",
                     "nature": "ordinal"
                 }
               },
               "mpg": {
                 "viewable": "false",
                 "label": {

                 }
               }
            }
        }

        var_display_modify = VariableDisplayUtil(self.test_input_01, update)
        var_err = var_display_modify.error_messages
        self.assertTrue(var_display_modify.has_error)
        print("Error : ", var_err)

    def test_90_update(self):
        """(90) test for error in updating non editable data"""
        """ here mean is not editable"""
        msgt(self.test_90_update.__doc__)
        update_json = {
            "preprocess_id": 45,
            "variable_updates": {
                "cylinders": {
                    "viewable": "true",
                    "omit": ["mean", "median"],
                    "value_updates": {
                        "numchar": "discrete",
                        "nature": "ordinal"
                    }
                },
                "mpg": {
                    "viewable": "false",
                    "omit": [],
                    "value_updates": {
                        "mean": 5

                    }
                }
            }
        }
        var_display_modify = VariableDisplayUtil(self.test_input_01, update_json)
        var_err = var_display_modify.get_error_messages()
        self.assertTrue(var_display_modify.has_error)
        print("Error : ", var_err)
