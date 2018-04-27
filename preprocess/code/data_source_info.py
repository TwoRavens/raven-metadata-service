from __future__ import print_function
import json
import col_info_constants as col_const
from collections import OrderedDict

SOURCE_TYPE_FILE = 'File'

class DataSourceInfo(object):

    def __init__(self, name, source_type, **kwargs):
        """Set data source"""
        self.name = name
        self.source_type = source_type
        self.source_format = kwargs.get('source_format')
        self.filesize = kwargs.get('filesize')

    def as_dict(self):
        """Return DataSourceInfo as an OrderedDict()"""
        data = OrderedDict()
        data['name'] = self.name
        data['type'] = self.source_type
        data['format'] = self.source_format

        if self.filesize:
            data['filesize'] = self.filesize

        return data
