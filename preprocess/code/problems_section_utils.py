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


    def problem_section_update(self):
        """update the preprocess with problem section """