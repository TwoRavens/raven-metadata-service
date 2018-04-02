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
        update_01_fname = join(TEST_DATA_DIR, 'update_org.json')
        preprocess_01_fname = join(TEST_DATA_DIR, 'preprocess_org.json')
        expected_01_fname = join(TEST_DATA_DIR,'expected_output.json')
        test_40_file = join(TEST_DATA_DIR, 'test_40_preprocess_file')
        update_data = open(update_01_fname, 'r').read()
        preprocess_data = open(preprocess_01_fname, 'r').read()
        self.expected_data = open(expected_01_fname,'r').read()
        test_40 = open(test_40_file,'r').read()
        self.update_json_01 = json.loads(update_data,
                                         object_pairs_hook=OrderedDict)
        self.preprocess_json_01 = json.loads(preprocess_data,
                                             object_pairs_hook=OrderedDict)

        self.test_40_file = json.loads(test_40, object_pairs_hook=OrderedDict)



    def test_10_update(self):
        """(10) Test the data for numeric series"""
        msgt(self.test_10_update.__doc__)

        self.assertTrue('preprocess_id' in self.update_json_01)
        # self.assertTrue('preprocess_id' in self.preprocess_json_01)


    def test_20_update(self):
        """(20) Test output json"""
        msgt(self.test_20_update.__doc__)
        var_util = VariableDisplayUtil(self.preprocess_json_01, self.update_json_01)

        success, var_display_util = True, var_util.get_updated_metadata()

        print(" ****output : ", var_display_util)
        print("**** exp_output : ", self.expected_data)

        expected_json = json.loads(self.expected_data,
                                   object_pairs_hook=OrderedDict)

        self.assertEqual(var_display_util, expected_json)


    def test_30_update(self):
        """(30) test if there is no error"""
        msgt(self.test_30_update.__doc__)
        var_display = VariableDisplayUtil(self.preprocess_json_01,self.update_json_01)
        self.assertTrue(var_display)

    def test_40_update(self):
        """(40) test for variable section not found in preprocess file"""
        msgt(self.test_40_update.__doc__)
        pre_file = self.test_40_file

        var_display_modify = VariableDisplayUtil(pre_file, self.update_json_01)
        var_err = var_display_modify.error_messages
        self.assertTrue(var_display_modify.has_error)
        print("Error : ",var_err)

    def test_50_update(self):
        """(50) test for variable display section not found in preprocess file"""
        msgt(self.test_50_update.__doc__)
        pre_file= {
               "$schema":"http://(link to eventual schema)/jjonschema/1-0-0#",
               "self":{
                  "description":"TwoRavens metadata generated by ....",
                  "created":"..time stamp..",
                  "preprocess_id":45,
                  "data_url":"http://metadata.2ravens-url.org/preprocess/data/45",
                  "format":"jsonschema",
                  "preprocess_version":"1-0-0",
                  "schema_version":"1.0.0"
               },
               "variables": {
                  "cylinders": {
                     "numchar":"continuous",
                      "nature": "nominal",
                     "mean":213,
                     "median":34

                  },
                  "mpg":{
                      "numchar": "continuous",
                       "nature": " ordinal",
                       "mean": 313,
                       "median": 54

                   }
               }
}
        var_display_modify = VariableDisplayUtil(pre_file, self.update_json_01)
        var_err = var_display_modify.error_messages
        self.assertTrue(var_display_modify.has_error)
        print("Error : ",var_err)

    def test_60_update(self):
        """(60) test for variable display section not found in preprocess file"""
        msgt(self.test_60_update.__doc__)
        update = {
            "preprocess_id": 45
        }
        var_display_modify = VariableDisplayUtil(self.preprocess_json_01, update)
        var_err = var_display_modify.error_messages
        self.assertTrue(var_display_modify.has_error)
        print("Error : ",var_err)

    def test_70_update(self):
        """(70) test for variable display section's viewable not found in update file"""
        msgt(self.test_70_update.__doc__)
        update = {
            "preprocess_id": 45,
            "variable_updates": {
               "cylinders" : {
                 "omit": ["mean", "median"],
                 "value_updates": {
                     "numchar":"discrete",
                     "nature": "ordinal"
                 }
               },
               "mpg": {
                 "viewable": "false",
                 "omit": [],
                 "label": {

                 }
               }
            }
        }

        var_display_modify = VariableDisplayUtil(self.preprocess_json_01, update)
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
                     "numchar":"discrete",
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

        var_display_modify = VariableDisplayUtil(self.preprocess_json_01, update)
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
        var_display_modify = VariableDisplayUtil(self.preprocess_json_01, update_json)
        var_err = var_display_modify.get_error_messages()
        self.assertTrue(var_display_modify.has_error)
        print("Error : ", var_err)
