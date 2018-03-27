"""Module for a variable's display settings"""
from collections import OrderedDict
import pandas as pd
from pandas.api.types import is_float_dtype, is_numeric_dtype
import json
import col_info_constants as col_const
from column_info import ColumnInfo
from np_json_encoder import NumpyJSONEncoder


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
        self.var_display();

    def add_error_message(self, err_msg):
        """Add error message"""
        print(err_msg)
        self.has_error = True
        self.error_messages.append(err_msg)

    @staticmethod
    def get_default_settings():
        """Return the initial preprocess settings"""
        return OrderedDict(viewable=True,
                           omit=[],
                           images=[])


    def var_display(self):
        """ this function go through the update_json and call omit,viewable,label functions"""
        update_json = self.update_file
        # print(update_json)
        self.original_json = self.preprocess_file

        if 'variables' in self.original_json:
            self.access_obj_original = self.original_json['variables']
        else:
            self.access_obj_original_display = None
            self.error_messages.append(
                "variables section is not found in Preprocess file")
            return ValueError

        if 'variable_display' in self.original_json:
            self.access_obj_original_display = self.original_json['variable_display']
        else:
            self.access_obj_original_display = None
            self.error_messages.append(
                'variable_display section is not found in Preprocess file')
            return ValueError

        if 'variable_updates' in update_json:
            access_object = update_json['variable_updates']
        else:
            access_object = None
            self.error_messages.append(
                'variable_updates not found in Update file')
            return ValueError


        self.col_names = list(self.access_obj_original)
        if self.access_obj_original_display and self.access_obj_original and access_object:
            # for each column say [' cylinder','mpg',...]
             for varname in self.col_names:

                 if 'omit' in access_object[varname]:
                    omit_object = access_object[varname]['omit']
                 else:
                     omit_object = None
                     self.error_messages.append(
                         "omit field not found in update file section of '%s'" % varname)
                     return ValueError

                 if 'viewable' in access_object[varname]:
                    viewable_object = access_object[varname]['viewable']
                 else:
                     viewable_object = None
                     self.error_messages.append(
                         "viewable field not found in update file section of '%s' " % varname)
                     return ValueError

                 if 'label' in access_object[varname]:
                    label_object = access_object[varname]['label']
                 else:
                     label_object = None
                     self.error_messages.append(
                         "label field not found in update file section of '%s'" % varname)
                     return ValueError

                 self.modify_original(varname, omit_object, viewable_object, label_object)

    def modify_original(self, varname, omit_obj, viewable_obj, label_obj):
        if not varname in self.access_obj_original:
            print('"%s" was not found in the "variable" section of the metadata file' % varname)
            self.error_messages.append('"%s" was not found in the "variable" section of the metadata file' % varname)
            return

        elif not varname in self.access_obj_original_display:
            print('"%s" was not found in the "variable_display" section of the metadata file' % varname)
            self.error_messages.append('"%s" was not found in the "variable_display" section of the metadata file' % varname)
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
            if viewable_obj and viewable_obj is False:
                # del self.access_obj_original[varname]
                display_variable_obj['viewable'] = "false"

            # code for label
            if label_obj:
                for att_name in self.attributes:
                    if att_name in label_obj and att_name in self.editable_vars:
                        variable_obj[att_name] = label_obj[att_name]

                display_variable_obj['label'] = label_obj


    def final_original_output(self):
        # print("json output : ",self.original_json)
        return json.dumps(self.original_json, indent=4, cls=NumpyJSONEncoder)
