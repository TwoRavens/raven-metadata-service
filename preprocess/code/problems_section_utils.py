from collections import OrderedDict
from decimal import Decimal
import pandas as pd
from django.utils.text import slugify
import re
from pandas.api.types import is_float_dtype, is_numeric_dtype
import json
import col_info_constants as col_const
from column_info import ColumnInfo
from np_json_encoder import NumpyJSONEncoder
from version_number_util import VersionNumberUtil

class ProblemSectionUtil(object):
    def __init__(self, preprocess_json, problem_section_json):
        """class for the problem section process"""

        assert isinstance(preprocess_json, dict),\
            "preprocess_json must be a dict/OrderedDict"

        self.preprocess_json = preprocess_json
        self.problem_section_json = problem_section_json

        # for error handling
        self.has_error = False
        self.error_messages = []
        self.original_json = None

    def add_error_message(self, err_msg):
        """Add error message"""
        # print(err_msg)
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
        print("Error messages ", self.error_messages)
        return self.error_messages

    @staticmethod
    def is_major_update():
        """add or change a custom stat"""
        return False

    @staticmethod
    def is_minor_update():
        """add or change a custom stat"""
        return True

    def redundent_id_check(self, id_list):
        list_preprocess_problem = list(self.preprocess_json[col_const.PROBLEM_KEY])
        print(list_preprocess_problem)
        for item in id_list:
            if item in list_preprocess_problem:
                self.add_error_message('%s ID already present' % item)
                return False, self.get_error_messages()
        return True, None

    def problem_section_update(self):
        """update the preprocess with problem section
        Sample problem_section_json:
        {
           "preprocessId":24,
           "version":1,
           "problems":
           [
              {
                 "description":{"problem_id":"problem1","system":"auto","meaningful":"no","target":"Hits",
                 "predictors":["At_bats","Runs","Doubles"],"transform":0,"subsetObs":0,"subsetFeats":0,
                 "task":"regression","rating":3,"description":"Hits is predicted by At_bats and Runs and Doubles",
                 "metric":"meanSquaredError"},
                 "results":{}
              }
           ]
        }
        """
        print(self.problem_section_json[col_const.PROBLEM_KEY])
        id_list = list(self.problem_section_json[col_const.PROBLEM_KEY])

        if col_const.PROBLEM_KEY not in self.preprocess_json:
            self.preprocess_json[col_const.PROBLEM_KEY] = self.problem_section_json[col_const.PROBLEM_KEY]
        else:
            success, obj = self.redundent_id_check(id_list)
            if not success:
                return False
            self.preprocess_json[col_const.PROBLEM_KEY].append(self.problem_section_json[col_const.PROBLEM_KEY])

        self.original_json = OrderedDict(self.preprocess_json)

        success, updated_or_err = VersionNumberUtil.update_version_number(
            self.original_json,
            self.is_major_update())

        if not success:
            self.add_error_message(updated_or_err)
            return False


