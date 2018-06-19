import pandas as pd
import numpy as np
import json
from collections import OrderedDict
import col_info_constants as col_const
from column_info import ColumnInfo
from basic_utils.basic_err_check import BasicErrCheck

import sys
from os.path import \
    (abspath, basename, dirname, isdir, isfile, join, splitext)

# Add preprocess code dir
PREPROCESS_DIR = join(dirname(dirname(dirname(abspath(__file__)))),
                      'metalearn',
                      'metalearn',
                      'metafeatures')
sys.path.append(PREPROCESS_DIR)
from metafeatures import Metafeatures
from column_info import ColumnInfo
from np_json_encoder import NumpyJSONEncoder
from column_info import ColumnInfo



class MetalearnUtil(object):

    def __init__(self, data_frame, col_info):
        """ to use metalearn submodule
        feature used : mean_categorical_attribute_entropy_time
        """
        print("***** Metalearn App*******")
        self.my_metafeatures = None
        self.has_error = False
        self.error_messages = []
        self.output_json = OrderedDict

        self.my_df = pd.DataFrame(data_frame)

        self.my_metafeatures = Metafeatures().compute(
            X=self.my_df,
            Y=None,  # supports None and only computes Y-independent mfs
            column_types=None,
            # column_types={
            #     'col_a': 'NUMERIC',
            #     'col_b': 'CATEGORICAL',
            #     'y': 'CATEGORICAL'
            # },
            # None for metafeature_ids means compute all available
            metafeature_ids=[
                "MeanCategoricalAttributeEntropy_Time"
            ],
            # metafeature_ids=None,
            sample_rows=True,  # samples down to 150k rows
            sample_columns=True,  # samples down to 150 cols
            seed=None,  # a seed will be generated randomly when None is given
            timeout=None  # will return those metafeatures computed within alloted time, in order of those requested
        )
        json_format = pd.DataFrame(self.my_metafeatures).to_json()
        print('***** METALEARN *****', json_format)
        self.colinfo.mean_categorical_attribute_entropy_time = json_format


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

        def get_error_messages(self):
            """Return the list of error messages"""
            return self.error_messages

        @staticmethod
        def get_output_json():
            return self.output_json



