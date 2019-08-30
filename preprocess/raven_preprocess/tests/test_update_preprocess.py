"""Unit testing for summary_stats_util using sample data"""
import unittest
from unittest import skip
from os.path import abspath, dirname, isfile, join
import json
import decimal
from collections import OrderedDict

import raven_preprocess.col_info_constants as col_const
import raven_preprocess.update_constants as update_const
from raven_preprocess.msg_util import dashes, msgt, msg
from raven_preprocess.variable_display_util import VariableDisplayUtil

TEST_DATA_DIR = join(dirname(abspath(__file__)), 'test_data')

class UpdatePreprocessTest(unittest.TestCase):
    """Unit testing class for summary_stats_util"""

    def get_file_content(self, fname, as_json_dict=True):

        full_filename = join(TEST_DATA_DIR, fname)
        assert isfile(full_filename),\
            'Set up file not found: %s' % full_filename

        with open(full_filename, 'r') as f: #.read()
            content = f.read()

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

    def test_010_update(self):
        """(10) Test the data for numeric series"""
        msgt(self.test_010_update.__doc__)

        self.assertTrue(col_const.PREPROCESS_ID in self.update_json_01)

    def test_020_clean_update(self):
        """(20) Test output json"""
        msgt(self.test_020_clean_update.__doc__)
        var_util = VariableDisplayUtil(self.test_input_01, self.update_json_01)

        #print('var_util.error_messages', var_util.error_messages)
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

    def test_040_update(self):
        """(40) test for variables section not found in preprocess file"""
        msgt(self.test_040_update.__doc__)
        preprocess_json = self.test_040_file

        var_util = VariableDisplayUtil(preprocess_json, self.update_json_01)
        print('var_util.error_messages', var_util.error_messages)

        self.assertTrue(var_util.has_error)

        expected_err = '"%s" section not found' % col_const.VARIABLES_SECTION_KEY
        var_err = var_util.get_error_messages()[0]

        print("Error: ", var_err)
        self.assertTrue(var_err.find(expected_err) > -1)


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


    def test_050_update(self):
        """(50) test for variable display section not found in preprocess file"""
        msgt(self.test_050_update.__doc__)

        var_display_modify = VariableDisplayUtil(self.test_050_input, self.update_json_01)
        var_err = var_display_modify.get_error_messages()[0]
        self.assertTrue(var_display_modify.has_error)

        print("Error: ", var_err)
        self.assertTrue(var_err.find(col_const.VARIABLE_DISPLAY_SECTION_KEY) > -1)
        self.assertTrue(var_err.find('not found') > -1)


    def test_060_update(self):
        """(60) test for variable display section not found in preprocess file"""
        msgt(self.test_060_update.__doc__)

        update = {col_const.PREPROCESS_ID: 5}
        var_display_modify = VariableDisplayUtil(self.test_input_01, update)
        #print('var_display_modify.get_error_messages()', var_display_modify.get_error_messages())
        var_err = var_display_modify.get_error_messages()[0]
        self.assertTrue(var_display_modify.has_error)

        self.assertTrue(var_err.find(update_const.VARIABLE_UPDATES) > -1)
        self.assertTrue(var_err.find('not found') > -1)


        print("Error: ", var_err)


    def test_070_update(self):
        """(70) should work w/o the viewable option"""
        msgt(self.test_070_update.__doc__)
        update = {
            col_const.PREPROCESS_ID: 5,
            update_const.VARIABLE_UPDATES: {
                "cylinders" : {
                     "omit": ["mean", "median"],
                     update_const.VALUE_UPDATES_KEY: {
                         "nature": "ordinal"
                 }
               },
               "mpg": {
                 "viewable": False,
                 "omit": [],
                 update_const.VALUE_UPDATES_KEY: {
                 }
               }
            }
        }

        var_util = VariableDisplayUtil(self.test_input_01, update)
        print('var_util errs', var_util.get_error_messages())

        self.assertTrue(var_util.has_error is False)


    def test_080_update(self):
        """(80) invalid value in the omit list"""
        msgt(self.test_080_update.__doc__)

        bumble_bee = 'bumble-bee'
        update = {
            col_const.PREPROCESS_ID: 5,
            update_const.VARIABLE_UPDATES: { \
               "cylinders": { \
                    "omit": ["mean", "median", bumble_bee],
                    update_const.VALUE_UPDATES_KEY: { \
                        "numchar": "discrete",
                        "nature": "ordinal"}},
               "mpg": { \
                 "viewable": False,
                 "label": {}}}}

        var_display_modify = VariableDisplayUtil(self.test_input_01, update)
        var_err = var_display_modify.get_error_messages()[0]
        self.assertTrue(var_display_modify.has_error)

        self.assertTrue(var_err.find(update_const.OMIT_KEY) > -1)
        self.assertTrue(var_err.find('does not exist') > -1)
        self.assertTrue(var_err.find(bumble_bee) > -1)


    def test_090_update(self):
        """(90) test for error in updating non editable data"""
        """In this case, "mean" is not editable"""
        msgt(self.test_090_update.__doc__)
        update_json = {
            col_const.PREPROCESS_ID: 5,
            update_const.VARIABLE_UPDATES: { \
                "cylinders": { \
                    "viewable": True,
                    "omit": ["mean", "median"],
                    update_const.VALUE_UPDATES_KEY: { \
                        "numchar": "character",
                        "nature": "ordinal"}},
                "mpg": { \
                    "viewable": False,
                    "omit": [],
                    update_const.VALUE_UPDATES_KEY: {
                        "mean": 5}}}}

        var_display_modify = VariableDisplayUtil(self.test_input_01, update_json)

        var_err = var_display_modify.get_error_messages()[0]
        self.assertTrue(var_display_modify.has_error)

        print("Error: ", var_err)
        self.assertTrue(var_err.find('is not editable') > -1)


    def test_100_update(self):
        """(100) Error b/c update has no real changes"""
        msgt(self.test_100_update.__doc__)
        update = {
            col_const.PREPROCESS_ID: 5,
            update_const.VARIABLE_UPDATES: { \
               "cylinders" : { \
                 "viewable": True,
                 "omit": [],
                 update_const.VALUE_UPDATES_KEY: { \
                     "nature": "ordinal"}}}}

        var_display_modify = VariableDisplayUtil(self.test_input_01, update)

        self.assertTrue(var_display_modify.has_error)

        var_err = var_display_modify.get_error_messages()[0]
        print("Error: ", var_err)
        self.assertTrue(var_err.find('A new version was NOT created') > -1)

    def test_110_update(self):
        """(110) Error for invalid nature and numchar values"""
        msgt(self.test_110_update.__doc__)

        invalid_nature = 'blue-footed-rhino'
        invalid_numchar = 'boogie-woogie'

        update = {
            col_const.PREPROCESS_ID: 5,
            update_const.VARIABLE_UPDATES: { \
               "cylinders" : { \
                 update_const.VALUE_UPDATES_KEY: { \
                     "nature": invalid_nature,
                     "numchar": invalid_numchar}}}}

        var_display_modify = VariableDisplayUtil(self.test_input_01, update)

        self.assertTrue(var_display_modify.has_error)

        var_err = var_display_modify.get_error_messages()
        print("Error: ", var_err)
        self.assertTrue(var_err[0].find('is not valid') > -1)
        self.assertTrue(var_err[1].find('is not valid') > -1)
