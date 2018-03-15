""" this is the information of dataset level info"""
import numpy as np
import pandas as pd
import re
import xmltodict
from np_json_encoder import NumpyJSONEncoder
from collections import OrderedDict

class DatasetLevelInfo(object):

    def __init__(self, metadataurl):
        self.metadataurl = metadataurl
        self.metadataflag = 1
        self.data = OrderedDict()
        self.data = {}
        self.file_desc = None
        self.study_desc = None
        self.vars = None

    def get_metadata(self):

        if self.metadataurl is not None or self.metadataurl is not "":
            self.metadataurl = re.sub("~/TwoRavens", "..", self.metadataurl)

            self.data = xmltodict.parse(self.metadataurl)   # convert the xml into dict
            self.study_desc = self.data['stdyDscr']
            self.file_desc = self.data['fileDscr']
            self.vars = self.data['dataDscr']

        # code for lablname











