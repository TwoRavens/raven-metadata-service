"""Unit testing for summary_stats_util using sample data"""
import unittest
from unittest import skip
from os.path import abspath, dirname, isfile, join
import json
from collections import OrderedDict
import col_info_constants as col_const

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
        self.test_020_expected_data = self.get_file_content('test_020_expected_data.json')

        self.update_json_01 = self.get_file_content('update_json_01.json')

        self.test_input_01 = self.get_file_content('test_input_01.json')

        self.test_040_file = self.get_file_content(\
                                    'test_040_preprocess_file.json',
                                    as_json_dict=False)

        self.test_050_input = self.get_file_content('test_050_input.json')

    def test_010_update(self):
        """(10) Test the data for numeric series"""
        msgt(self.test_010_update.__doc__)

        self.assertTrue(col_const.PREPROCESS_ID in self.update_json_01)


    def test_020_update(self):
        """(20) Test output json"""
        msgt(self.test_020_update.__doc__)
        var_util = VariableDisplayUtil(self.test_input_01, self.update_json_01)

        self.assertTrue(var_util.has_error is False)

        print(var_util.get_updated_metadata(True))
        self.assertEqual(json.dumps(var_util.get_updated_metadata()),
                         json.dumps(self.test_020_expected_data))


    @skip('skipit')
    def test_030_update(self):
        """(30) test if there is no error"""
        msgt(self.test_030_update.__doc__)
        var_display = VariableDisplayUtil(self.test_input_01,
                                          self.update_json_01)
        self.assertTrue(var_display)

    @skip('skipit')
    def test_040_update(self):
        """(40) test for variable section not found in preprocess file"""
        msgt(self.test_040_update.__doc__)
        pre_file = self.test_040_file

        var_display_modify = VariableDisplayUtil(pre_file, self.update_json_01)
        var_err = var_display_modify.error_messages
        self.assertTrue(var_display_modify.has_error)
        print("Error : ", var_err)

    @skip('skipit')
    def test_050_update(self):
        """(50) test for variable display section not found in preprocess file"""
        msgt(self.test_050_update.__doc__)

        var_display_modify = VariableDisplayUtil(self.test_050_input, self.update_json_01)
        var_err = var_display_modify.error_messages
        self.assertTrue(var_display_modify.has_error)

        print("Error : ", var_err)

    @skip('skipit')
    def test_060_update(self):
        """(60) test for variable display section not found in preprocess file"""
        msgt(self.test_060_update.__doc__)

        update = {"preprocess_id": 45}
        var_display_modify = VariableDisplayUtil(self.test_input_01, update)
        var_err = var_display_modify.error_messages
        self.assertTrue(var_display_modify.has_error)

        print("Error : ", var_err)


    @skip('skipit')
    def test_070_update(self):
        """(70) test for variable display section's viewable not found in update file"""
        msgt(self.test_070_update.__doc__)
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

    @skip('skipit')
    def test_080_update(self):
        """(80) test for variable display section's omit not found in update file"""
        msgt(self.test_080_update.__doc__)
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

    @skip('skipit')
    def test_090_update(self):
        """(90) test for error in updating non editable data"""
        """ here mean is not editable"""
        msgt(self.test_090_update.__doc__)
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

    @skip('skipit')
    def test_100_update(self):
        """(100) Don't allow invalid variables in "omit" """
        msgt(self.test_100_update.__doc__)
        update_json = {
                "preprocess_id": 45,
                "variable_updates": {
                    "cylinders": {
                        "omit": ["grinch", "flying-bees"],
                    }
                }
            }

        var_util = VariableDisplayUtil(self.test_input_01, update_json)

        self.assertTrue(var_util.has_error)
        print(var_util.get_error_messages())
        return
        var_display_util = var_util.get_updated_metadata()

        #self.assertTrue(success)
        self.assertEqual(var_display_util, self.test_020_expected_data)
