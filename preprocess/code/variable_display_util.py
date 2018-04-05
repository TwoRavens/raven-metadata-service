"""Module for a variable's display settings"""
from collections import OrderedDict
import pandas as pd
from pandas.api.types import is_float_dtype, is_numeric_dtype
import json
import col_info_constants as col_const
import update_constants as update_const
from column_info import ColumnInfo
from np_json_encoder import NumpyJSONEncoder

ALL_VARIABLE_ATTRIBUTES = [x[0] for x in ColumnInfo.get_variable_labels()]
EDITABLE_ATTRIBUTES = ColumnInfo.get_editable_column_labels()

class VariableDisplayUtil(object):


    def __init__(self, preprocess_json, update_json):
        """Init with a pandas dataframe"""
        assert isinstance(preprocess_json, dict),\
            "preprocess_json must be a dict/OrderedDict"
        assert isinstance(update_json, dict),\
            "update_json must be a dict/OrderedDict"

        self.preprocess_json = preprocess_json
        self.update_json = update_json

        # count the updates
        self.update_cnt = 0

        # for error handling
        self.has_error = False
        self.error_messages = []
        self.original_json = None
        self.access_obj_original = None
        self.access_obj_original_display = None

        # call the display function
        self.update_preprocess_data()

    def add_error_message(self, err_msg):
        """Add error message"""
        print(err_msg)
        self.has_error = True
        self.error_messages.append(err_msg)

    def get_updated_metadata(self, as_string=False):
        """Return the modified metadata--which is in the 'original_json' """
        assert self.has_error is False, \
              "Make sure that 'has_error' is False before using this method"

        if as_string:
            return json.dumps(self.original_json, indent=4, cls=NumpyJSONEncoder)

        return self.original_json

    @staticmethod
    def get_default_settings():
        """Return the initial preprocess settings"""
        return OrderedDict(viewable=True,
                           omit=[],
                           images=[])


    def get_error_messages(self):
        """Return the list of error messages"""
        return self.error_messages


    def run_basic_checks(self):
        """Do some sanity checks--replace this with JSON schema checks..."""
        if col_const.PREPROCESS_ID not in self.update_json:
            self.add_error_message(\
                "A '%s' was not found in the update JSON" % col_const.PREPROCESS_ID)
            return False

        if col_const.SELF_SECTION_KEY not in self.preprocess_json:
            self.add_error_message(\
                "A '%s' was not found in the preprocess JSON" % col_const.SELF_SECTION_KEY)
            return False

        if col_const.PREPROCESS_ID not in self.preprocess_json[col_const.SELF_SECTION_KEY]:
            self.add_error_message(\
                "A '%s.%s' was not found in the preprocess JSON" % \
                (col_const.SELF_SECTION_KEY, col_const.PREPROCESS_ID))
            return False

        if not self.update_json[col_const.PREPROCESS_ID] == \
            self.preprocess_json[col_const.SELF_SECTION_KEY][col_const.PREPROCESS_ID]:
            self.add_error_message(\
                ('The "{0}" in the update does not match the'
                 ' "{1}.{0}" in the preprocess metadata').format(\
                 col_const.PREPROCESS_ID, col_const.SELF_SECTION_KEY))
            return False

        if col_const.VARIABLES_SECTION_KEY in self.preprocess_json:
            self.access_obj_original = self.preprocess_json[col_const.VARIABLES_SECTION_KEY]
        else:
            self.add_error_message(
                '"%s" section not found in the preprocess data' % col_const.VARIABLES_SECTION_KEY)
            return False

        if col_const.VARIABLE_DISPLAY_SECTION_KEY in self.preprocess_json:
            self.access_obj_original_display = \
                self.preprocess_json[col_const.VARIABLE_DISPLAY_SECTION_KEY]
        else:
            self.add_error_message(\
                '"%s" section not found in the preprocess data' % \
                col_const.VARIABLE_DISPLAY_SECTION_KEY)
            return False


        return True

    def update_preprocess_data(self):
        """Iterate through the update_json and call omit,viewable,label functions"""
        if not self.run_basic_checks():
            return False, self.get_error_messages

        self.original_json = self.preprocess_json

        if update_const.VARIABLE_UPDATES in self.update_json:
            variable_updates = self.update_json[update_const.VARIABLE_UPDATES]
        else:
            variable_updates = None
            self.add_error_message(
                'variable_updates not found in Update file')
            return False, self.get_error_messages()


        # Iterate through the columns and make updates
        #
        cols_to_update = list(variable_updates)
        for varname in cols_to_update:

            # Check for changes to the omit list
            #
            if update_const.OMIT_KEY in variable_updates[varname]:
                self.update_omit_list(\
                        varname,
                        variable_updates[varname][update_const.OMIT_KEY])

            if update_const.VIEWABLE_KEY in variable_updates[varname]:
                self.update_viewable(\
                        varname,
                        variable_updates[varname][update_const.VIEWABLE_KEY])

            if update_const.VALUE_UPDATES_KEY in variable_updates[varname]:
                value_update_dict = variable_updates[varname][update_const.VALUE_UPDATES_KEY]
            else:
                value_update_dict = None

            self.modify_original(varname, value_update_dict)

        # Check if any updates were made...
        #
        print('self.update_cnt', self.update_cnt)
        if self.update_cnt == 0:
            user_msg = ('The update request will not change'
                        ' the current preprocess metadata.'
                        ' A new version was NOT created')
            self.add_error_message(user_msg)

        if self.has_error:
            return False, self.get_error_messages()

        return True, self.get_updated_metadata()


    def update_viewable(self, varname, viewable_val):
        """Update the viewable parameter within the variable display section"""
        assert self.access_obj_original_display is not None,\
            ('The self.access_obj_original_display must'
             ' be populated before using this method')
        assert varname in self.access_obj_original_display,\
            ('The self.access_obj_original_display must'
             ' contain the "varname" as a key to use this method.'
             ' e.g. please check beforehand')

        if viewable_val is None:
            return

        # Is it a legimate value?
        if viewable_val not in (True, False):
            user_msg = ('For variable "%s" the value for "%s" must'
                        ' be "true" or "false"'
                        ' (Hint: make sure it is not a string)') % \
                        (varname, update_const.VIEWABLE_KEY)
            self.add_error_message(user_msg)
            return

        # Is it an update?
        if self.access_obj_original_display[varname][update_const.VIEWABLE_KEY] ==\
            viewable_val:
            # Same value, no update to make
            return

        self.update_cnt += 1
        self.access_obj_original_display[varname][update_const.VIEWABLE_KEY] = \
            viewable_val


    def update_omit_list(self, varname, omit_list):
        """Update the omit_list in the preprocess metadata.  """
        assert self.access_obj_original_display is not None,\
            ('The self.access_obj_original_display must'
             ' be populated before using this method')
        assert varname in self.access_obj_original_display,\
            ('The self.access_obj_original_display must'
             ' contain the "varname" as a key to use this method.'
             ' e.g. please check beforehand')

        if omit_list is None:
            return

        # Make sure all of the omit variables are valid
        #
        err_found = False
        for omit_var in omit_list:
            if omit_var not in ALL_VARIABLE_ATTRIBUTES:
                err_found = True
                err_msg = ('Variable "%s", which is in the %s list for'
                           ' %s does not exist.') %\
                           (omit_var, update_const.OMIT_KEY, varname)
                self.add_error_message(err_msg)

        orig_omit_var = self.access_obj_original_display[varname][update_const.OMIT_KEY]

        if not err_found:
            if set(orig_omit_var) ==\
                set(omit_list):
                # nothing to change, keep going
                pass
            else:
                orig_omit_var = omit_list
                self.update_cnt += 1


    def modify_original(self, varname, value_update_dict):
        """Make updates to the original preprocess file for a single variable"""

        #print(self.access_obj_original_display)

        # ---------------------------------
        # Look for the variable in the original variables section
        # ---------------------------------
        if not varname in self.access_obj_original:
            err_msg = ('"%s" was not found in the "%s"'
                       ' section of the metadata file') % \
                       (varname, col_const.VARIABLES_SECTION_KEY)
            self.add_error_message(err_msg)
            return

        elif not varname in self.access_obj_original_display:
            # ---------------------------------
            # Look for the variable in the original variable_display section
            # ---------------------------------
            err_msg = ('"%s" was not found in the "%s"'
                       ' section of the metadata file') % \
                       (varname, col_const.VARIABLE_DISPLAY_SECTION_KEY)
            self.add_error_message(err_msg)
            return

        # ---------------------------------
        # Let's make the updates...
        # ---------------------------------

        # 'variables' section of preprocess
        variable_obj = self.access_obj_original[varname]
        # 'variable_display' section of preprocess
        display_variable_obj = self.access_obj_original_display[varname]


        # ---------------------------------
        # Update variable values....
        # ---------------------------------
        if value_update_dict:
            for update_var, update_value in value_update_dict.items():
                if update_var not in EDITABLE_ATTRIBUTES:
                    err_msg = ('For the variable "%s", the value for "%s"'
                               ' is not editable.  Editable variables are:'
                               ' %s') % \
                               (varname, update_var, EDITABLE_ATTRIBUTES)
                    self.add_error_message(err_msg)

                elif update_var == col_const.NATURE_LABEL:
                    if not ColumnInfo.is_valid_nature(update_value):
                        err_msg = ('For the variable "%s", the value for "%s"'
                                   ' is not valid.  Valid values are:'
                                   ' %s') % \
                            (varname, col_const.NATURE_LABEL, col_const.NATURE_VALUES)
                        self.add_error_message(err_msg)

                elif update_var == col_const.NUMCHAR_LABEL:
                    if not ColumnInfo.is_valid_numchar(update_value):
                        err_msg = ('For the variable "%s", the value for "%s"'
                                   ' is not valid.  Valid values are:'
                                   ' %s') % \
                            (varname, col_const.NUMCHAR_LABEL, col_const.NUMCHAR_VALUES)
                        self.add_error_message(err_msg)

                elif variable_obj[update_var] == update_value:
                    # No change needed
                    pass
                else:
                    variable_obj[update_var] = update_value
                    self.update_cnt += 1
            #import ipdb; ipdb.set_trace()
            #display_variable_obj[update_const.VALUE_UPDATES_KEY] = label_obj
