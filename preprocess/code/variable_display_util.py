"""Module for a variable's display settings"""
from collections import OrderedDict
import pandas as pd
from pandas.api.types import is_float_dtype, is_numeric_dtype
import json
import col_info_constants as col_const
from column_info import ColumnInfo
from np_json_encoder import NumpyJSONEncoder

VALUE_UPDATES = 'value_updates'


class VariableDisplayUtil(object):


    def __init__(self,preprocess_file, update_file):
        """Init with a pandas dataframe"""
        assert preprocess_file or update_file is not None, "files can't be None"

        self.preprocess_file = preprocess_file
        self.update_file = update_file
        self.col_names = {}
        # Initial settings


        self.attributes = [x[0] for x in ColumnInfo.get_variable_labels()]  # list of all the attributes ***
        self.editable_vars = ColumnInfo.get_editable_column_labels()      # list of all the attributes set as editable ***

        # for error handling
        self.has_error = False
        self.error_messages = []
        self.original_json = {}
        self.access_obj_original= {}
        self.access_obj_original_display = {}
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
        return self.error_messages



    def update_preprocess_data(self):
        """ this function go through the update_json and call omit,viewable,label functions"""
        update_json = self.update_file
        # print(update_json)
        self.original_json = self.preprocess_file

        if 'variables' in self.original_json:
            self.access_obj_original = self.original_json['variables']
        else:
            self.access_obj_original_display = None
            self.add_error_message(
                "variables section is not found in Preprocess file")
            return False, self.get_error_messages()

        if 'variable_display' in self.original_json:
            self.access_obj_original_display = self.original_json['variable_display']
        else:
            self.access_obj_original_display = None
            self.add_error_message(
                'variable_display section is not found in Preprocess file')
            return False, self.get_error_messages()

        if 'variable_updates' in update_json:
            access_object = update_json['variable_updates']
        else:
            access_object = None
            self.add_error_message(
                'variable_updates not found in Update file')
            return False, self.get_error_messages()


        self.col_names = list(access_object)
        print('self.col_names', self.col_names)
        if self.access_obj_original_display and self.access_obj_original and access_object:
            # for each column say [' cylinder','mpg',...]
             for varname in self.col_names:
                 print('varname', varname)
                 if 'omit' in access_object[varname]:
                    omit_object = access_object[varname]['omit']
                 else:
                     omit_object = None
                     self.add_error_message(
                         "omit field not found in update file section of '%s'" % varname)
                     return False, self.get_error_messages()

                 if 'viewable' in access_object[varname]:
                    viewable_object = access_object[varname]['viewable']
                 else:
                     viewable_object = None
                     self.add_error_message(
                         "viewable field not found in update file section of '%s' " % varname)
                     return False, self.get_error_messages()

                 if VALUE_UPDATES in access_object[varname]:
                    label_object = access_object[varname][VALUE_UPDATES]
                 else:
                     label_object = None


                 self.modify_original(varname, omit_object, viewable_object, label_object)
        if self.has_error:
            return False, self.get_error_messages()
        else:
            return True, self.final_original_output()

    def modify_original(self, varname, omit_obj, viewable_obj, label_obj):
        print(self.access_obj_original_display)
        if not varname in self.access_obj_original:
            print('"%s" was not found in the "variable" section of the metadata file' % varname)
            self.add_error_message('"%s" was not found in the "variable" section of the metadata file' % varname)
            return

        elif not varname in self.access_obj_original_display:
            print('"%s" was not found in the "variable_display" section of the metadata file' % varname)
            self.add_error_message('"%s" was not found in the "variable_display" section of the metadata file' % varname)
            return

        else:

            variable_obj = self.access_obj_original[varname]
            display_variable_obj = self.access_obj_original_display[varname]
            # print(variable_obj)
            """
            variable_obj contains : "numchar":"continuous",
                        "nature": "nominal",
                       "mean":213,
                       "median":34
            """
            # code for omit
            if omit_obj:
                # start deleting omit objects
                # for omit_var in omit_obj:
                #      del variable_obj[omit_var]
                display_variable_obj['omit'] = omit_obj

            # code for viewable
            print("viewable obj ",viewable_obj)
            if viewable_obj == False:
                # del self.access_obj_original[varname]
                display_variable_obj['viewable'] = False

            # code for label
            if label_obj:
                for att_name in label_obj:
                    if att_name not in self.editable_vars:
                        self.add_error_message(" '%s' is not editable" % att_name)
                    else:
                        variable_obj[att_name] = label_obj[att_name]


                display_variable_obj[VALUE_UPDATES] = label_obj


    def final_original_output(self):
        # print("json output : ",self.original_json)
        output = json.dumps(self.original_json, indent=4, cls=NumpyJSONEncoder)
        if self.has_error:
            return False, self.error_messages
        else:
            return True, output
