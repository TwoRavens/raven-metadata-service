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
VIEWABLE_VALUES = [True, False]
CUSTOM_STATISTICS_NAME = 'name'
CUSTOM_STATISTICS_VARIABLES = 'variables'
CUSTOM_STATISTICS_IMAGE = 'image'
CUSTOM_STATISTICS_DESCRIPTION = 'description'
CUSTOM_STATISTICS_REPLICATION = 'replication'
CUSTOM_STATISTICS_VIEWABLE = 'viewable'

class CustomStatisticsUtil(object):
    def __init__(self,preprocess_json, custom_statistics_json):
        """class for the custom statistics process"""
        """
        sample Update json coming :
        {
   "preprocess_id":1677,
   "custom_statistics":[
      {
         "name":"Third order statistic",
         "variables":"lpop,bebop",
         "image":"http://www.google.com",
         "value":23.45,
         "description":"Third smallest value",
         "replication":"sorted(X)[2]",
         "omit":false
      },
      {
         "name":"Fourth order statistic",
         "variables":"pop,bebop",
         "image":"http://www.youtube.com",
         "value":29.45,
         "description":"Fourth smallest value",
         "replication":"sorted(X)[3]",
         "omit":false
      }
   ]
}
        """

        assert isinstance(preprocess_json, dict), \
            "preprocess_json must be a dict/OrderedDict"


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
        print("Error messages ",self.error_messages)
        return self.error_messages

    def update_preprocess_version(self):
        """ here update the preprocess version of the metadata"""

    def custom_statistics_create_id(self): # need to think of generating id
        if col_const.CUSTOM_KEY not in self.preprocess_json:
            var_id = 'id_000001'
        else:
            ids = list(self.preprocess_json['custom_statistics'])
            ids.sort()
            latest_id = ids[-1]
            _unused, idnum = latest_id.split('_')
            next_num = str(int(idnum) + 1)
            var_id = 'id_%s' % next_num.zfill(6)
        return var_id

    def custom_statistics_check_name(self,name):
        statistics_name = name
        if not re.match(r'^[A-Za-z0-9_ ]+$', statistics_name): # check if the name is alpha numerics , \
                                      #  i.e does not contain special characters or empty spaces
            self.add_error_message('The name is not alpha-numeric')
        # if col_const.CUSTOM_KEY in self.preprocess_json:
            # for val in self.preprocess_json[col_const.CUSTOM_KEY]:
            #     print("Value coming ",self.preprocess_json[col_const.CUSTOM_KEY][val]['name'])
            #     if name == self.preprocess_json[col_const.CUSTOM_KEY][val]['name']:
            #         print("******** error **********")
            #         self.add_error_message('The variable name %s already exist in the metadata file' % name)
        return statistics_name

    def custom_statistics_check_variables(self,var_list,variables):
        print("all var ", var_list)
        for var in variables:
            if var not in var_list:
                self.add_error_message('The variable %s does not exist in the metadata file' % var )

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

    def custom_statistics_check_viewable(self,viewable):
        if viewable not in VIEWABLE_VALUES:
            self.add_error_message('Viewable should be either True or False')
            return
        return viewable


    def custom_statistics_update(self):
        """Main function for appending the data"""
        # print(self.preprocess_json)
        print("custom statistics json ",self.custom_statistics_json)


        # preprocess_id = self.custom_statistics_json['preprocess_id']
        var_list = list(self.preprocess_json['variables'])
        for dat in self.custom_statistics_json:
            print("dat ",dat)
            name = self.custom_statistics_check_name(dat['name']) # required = True
            # id = self.custom_statistics_create_id(name)
            variables = self.custom_statistics_check_variables(var_list,dat['variables']) # required = True

            if CUSTOM_STATISTICS_IMAGE in dat:
                image = self.custom_statistics_check_image(dat['image'])
            else:
                image =[]

            value = self.custom_statistics_check_value(dat['value']) # required = True

            if CUSTOM_STATISTICS_DESCRIPTION in dat:
                description = self.custom_statistics_check_description(dat['description'])
            else:
                description = ""

            if CUSTOM_STATISTICS_REPLICATION in dat:
                replication = self.custom_statistics_check_replication(dat['replication'])
            else:
                replication = ""

            if CUSTOM_STATISTICS_VIEWABLE in dat:
                viewable = self.custom_statistics_check_viewable(dat['viewable'])
            else:
                viewable = True # default

            data = {
                    "name":name,
                    "variables":variables,
                    "image":image,
                    "value":value,
                    "description":description,
                    "replication":replication,
                    "display": {
                        "viewable":viewable
                    }

                }


            # print("data to be sent",data)

            self.add_to_original(data)

        self.original_json = OrderedDict(self.preprocess_json)


    def add_to_original(self,data):
        id = self.custom_statistics_create_id()
        # self.original_json= self.preprocess_json
        if col_const.CUSTOM_KEY not in self.preprocess_json:
            self.preprocess_json[col_const.CUSTOM_KEY] = { id: data}
        else:
            self.preprocess_json[col_const.CUSTOM_KEY][id]= data


        # print(self.original_json)





