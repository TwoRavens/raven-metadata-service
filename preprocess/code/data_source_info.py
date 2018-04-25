from __future__ import print_function
import json
import col_info_constants as col_const
from collections import OrderedDict

SOURCE_TYPE_FILE = 'File'

class DataSourceInfo(object):

    def __init__(self, name, source_type, source_format=None):
        """set data source"""
        self.name = name
        self.source_type = source_type
        self.source_format = source_format

    def as_dict(self):
        """Return this as an OrderedDict()"""
        data = OrderedDict()
        data['name'] = self.name
        data['type'] = self.source_type
        data['format'] = self.source_format

        return data
