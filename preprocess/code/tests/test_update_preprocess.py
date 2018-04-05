"""Unit testing for summary_stats_util using sample data"""
import unittest
from unittest import skip
from os.path import abspath, dirname, isfile, join
import json
import decimal
from collections import OrderedDict
import col_info_constants as col_const
import update_constants as update_const

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
                          object_pairs_hook=OrderedDict,
                          parse_float=decimal.Decimal)

    def setUp(self):
        """Load up tests as OrderedDict objects--unless specified otherwise"""
        self.expected_data_01 = self.get_file_content('expected_data_01.json')

        self.update_json_01 = self.get_file_content('update_json_01.json')

        self.test_input_01 = self.get_file_content('test_input_01.json')

        self.test_040_file = self.get_file_content(\
                                    'test_040_preprocess_file.json')

        self.test_050_input = self.get_file_content('test_050_input.json')

    #@skip('skipit')
    def test_010_update(self):
        """(10) Test the data for numeric series"""
        msgt(self.test_010_update.__doc__)

        self.assertTrue(col_const.PREPROCESS_ID in self.update_json_01)


    #@skip('skipit')
    def test_020_clean_update(self):
        """(20) Test output json"""
        msgt(self.test_020_clean_update.__doc__)
        var_util = VariableDisplayUtil(self.test_input_01, self.update_json_01)

        self.assertTrue(var_util.has_error is False)

        #print('=' * 40)
        #print(var_util.get_updated_metadata(True))
        #print('=' * 40)

        updated_metadata = var_util.get_updated_metadata()
        self.assertEqual(updated_metadata,
                         self.expected_data_01)

        version = updated_metadata[col_const.SELF_SECTION_KEY][col_const.VERSION_KEY]
        print('new version', version)
        self.assertEqual(version, 2)

    #@skip('skipit')
    def test_040_update(self):
        """(40) test for variables section not found in preprocess file"""
        msgt(self.test_040_update.__doc__)
        preprocess_json = self.test_040_file

        var_display_modify = VariableDisplayUtil(preprocess_json, self.update_json_01)
        self.assertTrue(var_display_modify.has_error)

        expected_err = '"%s" section not found' % col_const.VARIABLES_SECTION_KEY
        var_err = var_display_modify.get_error_messages()[0]

        print("Error: ", var_err)
        self.assertTrue(var_err.find(expected_err) > -1)


    #@skip('skipit')
    def test_045_update_err(self):
        """(45) test for preprocess id's not matching"""
        msgt(self.test_045_update_err.__doc__)
        update_json = self.update_json_01

        update_json[col_const.PREPROCESS_ID] = 999

        var_display_modify = VariableDisplayUtil(self.test_input_01, update_json)
        self.assertTrue(var_display_modify.has_error)

        var_err = var_display_modify.get_error_messages()[0]

        print("Error: ", var_err)
        self.assertTrue(var_err.find(col_const.PREPROCESS_ID) > -1)
        self.assertTrue(var_err.find('does not match') > -1)


    #@skip('skipit')
    def test_050_update(self):
        """(50) test for variable display section not found in preprocess file"""
        msgt(self.test_050_update.__doc__)

        var_display_modify = VariableDisplayUtil(self.test_050_input, self.update_json_01)
        var_err = var_display_modify.get_error_messages()[0]
        self.assertTrue(var_display_modify.has_error)

        print("Error: ", var_err)
        self.assertTrue(var_err.find(col_const.VARIABLE_DISPLAY_SECTION_KEY) > -1)
        self.assertTrue(var_err.find('not found') > -1)


    #@skip('skipit')
    def test_060_update(self):
        """(60) test for variable display section not found in preprocess file"""
        msgt(self.test_060_update.__doc__)

        update = {"preprocess_id": 5}
        var_display_modify = VariableDisplayUtil(self.test_input_01, update)
        var_err = var_display_modify.get_error_messages()[0]
        self.assertTrue(var_display_modify.has_error)

        self.assertTrue(var_err.find(update_const.VARIABLE_UPDATES) > -1)
        self.assertTrue(var_err.find('not found') > -1)


        print("Error: ", var_err)


    #@skip('skipit')
    def test_070_update(self):
        """(70) should work w/o the viewable option"""
        msgt(self.test_070_update.__doc__)
        update = {
            "preprocess_id": 5,
            "variable_updates": {
               "cylinders" : {
                 "omit": ["mean", "median"],
                 "value_updates": {
                     "nature": "ordinal"
                 }
               },
               "mpg": {
                 "viewable": False,
                 "omit": [],
                 "value_updates": {
                 }
               }
            }
        }

        var_util = VariableDisplayUtil(self.test_input_01, update)
        print('var_util errs', var_util.get_error_messages())

        self.assertTrue(var_util.has_error is False)


    #@skip('skipit')
    def test_080_update(self):
        """(80) invalid value in the omit list"""
        msgt(self.test_080_update.__doc__)

        bumble_bee = 'bumble-bee'
        update = {
            "preprocess_id": 5,
            "variable_updates": {
               "cylinders" : {
                 "omit": ["mean", "median", bumble_bee],
                 "value_updates": {
                     "numchar": "discrete",
                     "nature": "ordinal"
                 }
               },
               "mpg": {
                 "viewable": False,
                 "label": {

                 }
               }
            }
        }

        var_display_modify = VariableDisplayUtil(self.test_input_01, update)
        var_err = var_display_modify.get_error_messages()[0]
        self.assertTrue(var_display_modify.has_error)

        self.assertTrue(var_err.find(update_const.OMIT_KEY) > -1)
        self.assertTrue(var_err.find('does not exist') > -1)
        self.assertTrue(var_err.find(bumble_bee) > -1)


    #@skip('skipit')
    def test_090_update(self):
        """(90) test for error in updating non editable data"""
        """In this case, "mean" is not editable"""
        msgt(self.test_090_update.__doc__)
        update_json = {
            "preprocess_id": 5,
            "variable_updates": {
                "cylinders": {
                    "viewable": True,
                    "omit": ["mean", "median"],
                    "value_updates": {
                        "numchar": "character",
                        "nature": "ordinal"
                    }
                },
                "mpg": {
                    "viewable": False,
                    "omit": [],
                    "value_updates": {
                        "mean": 5

                    }
                }
            }
        }

        var_display_modify = VariableDisplayUtil(self.test_input_01, update_json)

        var_err = var_display_modify.get_error_messages()[0]
        self.assertTrue(var_display_modify.has_error)

        print("Error: ", var_err)
        self.assertTrue(var_err.find('is not editable') > -1)


    #@skip('skipit')
    def test_100_update(self):
        """(100) Error b/c update has no real changes"""
        msgt(self.test_100_update.__doc__)
        update = {
            "preprocess_id": 5,
            "variable_updates": {
               "cylinders" : {
                 "viewable": True,
                 "omit": [],
                 "value_updates": {
                     "nature": "ordinal"
                     }
                }
            }
        }

        var_display_modify = VariableDisplayUtil(self.test_input_01, update)

        self.assertTrue(var_display_modify.has_error)

        var_err = var_display_modify.get_error_messages()[0]
        print("Error: ", var_err)
        self.assertTrue(var_err.find('A new version was NOT created') > -1)

    #@skip('skipit')
    def test_110_update(self):
        """(110) Error for invalid nature and numchar values"""
        msgt(self.test_110_update.__doc__)

        invalid_nature = 'blue-footed-rhino'
        invalid_numchar = 'boogie-woogie'

        update = {
            "preprocess_id": 5,
            "variable_updates": {
               "cylinders" : {
                 "value_updates": {
                     "nature": invalid_nature,
                     "numchar": invalid_numchar
                     }
                }
            }
        }

        var_display_modify = VariableDisplayUtil(self.test_input_01, update)

        self.assertTrue(var_display_modify.has_error)

        var_err = var_display_modify.get_error_messages()
        print("Error: ", var_err)
        self.assertTrue(var_err[0].find('is not valid') > -1)
        self.assertTrue(var_err[1].find('is not valid') > -1)
