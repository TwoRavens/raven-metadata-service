""" File to get the updated metadata file with custom statistics"""
from collections import OrderedDict
from decimal import Decimal
import pandas as pd
from django.utils.text import slugify
import re
from pandas.api.types import is_float_dtype, is_numeric_dtype
import json, uuid
from random import randrange
import col_info_constants as col_const
import update_constants as update_const
from column_info import ColumnInfo
from np_json_encoder import NumpyJSONEncoder

ALL_VARIABLE_ATTRIBUTES = [x[0] for x in ColumnInfo.get_variable_labels()]
OMIT_VALUES = ['True', 'False']
class CustomStatisticsUtil(object):
    def __init__(self,preprocess_json, custom_statistics_json):
        """class for the custom statistics process"""
        assert isinstance(preprocess_json, dict), \
            "preprocess_json must be a dict/OrderedDict"
        assert isinstance(custom_statistics_json, dict), \
            "update_json must be a dict/OrderedDict"

        self.preprocess_json = preprocess_json
        self.custom_statistics_json = custom_statistics_json

        # for error handling
        self.has_error = False
        self.error_messages = []
        self.original_json=None

        # call the statistic function
        self.custom_statistics_update()


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
            return json.dumps(self.original_json,
                              indent=4,
                              cls=NumpyJSONEncoder)

        return self.original_json

    def get_error_messages(self):
        """Return the list of error messages"""
        return self.error_messages

    def update_preprocess_version(self):
        """ here update the preprocess version of the metadata"""

    def custom_statistics_create_id(self,name): # need to think of generating id
        var_id = slugify(name).replace('-', '_')[:25]

        return var_id

    def custom_statistics_check_name(self,name):
        statistics_name = name
        if not re.match(r'^[A-Za-z0-9_ ]+$', statistics_name): # check if the name is alpha numerics , \
                                      #  i.e does not contain special characters or empty spaces
            self.add_error_message('The name is not alpha-numeric')
        return statistics_name

    def custom_statistics_check_variables(self,var_list,variables):
        print("all var ", var_list)
        if variables not in var_list:
            self.add_error_message('The variable does not exist in the metadata file')

        return variables

    def custom_statistics_check_image(self,image_url):
        if image_url is None:
            self.add_error_message('image url is none')

        return image_url

    def is_major_update(self):
        """add or change a custom stat"""
        return False

    def is_minor_update(self):
        """add or change a custom stat"""
        return True

    def custom_statistics_check_value(self,value):
        if value is None:
            self.add_error_message(' value is none ')

        return value

    def custom_statistics_check_description(self,desc):
        if desc is None:
            self.add_error_message(' value is none ')
            return

        return desc

    def custom_statistics_check_replication(self,rep):
        if rep is None:
            self.add_error_message(' value is none ')
            return

        return rep

    def custom_statistics_check_omit(self,omit):
        if omit not in OMIT_VALUES:
            self.add_error_message('Omit should be either True or False')
            return
        return omit

    def custom_statistics_update(self):
        """Main function for appending the data"""
        # print(self.preprocess_json)
        # print(self.custom_statistics_json['variables'])
        preprocess_id = self.custom_statistics_json['preprocess_id']
        var_list = list(self.preprocess_json['variables'])
        name = self.custom_statistics_check_name(self.custom_statistics_json['name'])
        variables = self.custom_statistics_check_variables(var_list,self.custom_statistics_json['variables'])
        image = self.custom_statistics_check_image(self.custom_statistics_json['image'])
        value = self.custom_statistics_check_value(self.custom_statistics_json['value'])
        description = self.custom_statistics_check_description(self.custom_statistics_json['description'])
        replication = self.custom_statistics_check_replication(self.custom_statistics_json['replication'])
        omit = self.custom_statistics_check_omit(self.custom_statistics_json['omit'])

        data = {
                "name":name,
                "variables":[variables],
                "image":[image],
                "value":value,
                "description":description,
                "replication":replication,
                "display": {
                    "omit":omit
                }

        }
        print("data to be sent",data)

        self.add_to_original(data)

    def add_to_original(self,data):
        id = self.custom_statistics_create_id(data['name'])
        # self.original_json= self.preprocess_json
        if id is 1:
            self.preprocess_json[col_const.CUSTOM_KEY] = { id: data}
        else:
            self.preprocess_json[col_const.CUSTOM_KEY][id]= data

        self.original_json = self.preprocess_json
        # print(self.original_json)





