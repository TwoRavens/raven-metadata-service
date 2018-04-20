from __future__ import print_function
import json
import col_info_constants as col_const
from collections import OrderedDict


class DataSourceInfo(object):

    def __init__(self, **kwargs):
        """ set data source"""

        self.name = kwargs.get('name')
        self.type = kwargs.get('type')
        self.format = kwargs.get('format')
        self.data = None
        self.to_dict()

    def to_dict(self):
        self.data = OrderedDict()
        self.data['type'] = self.type
        self.data['format'] = self.format
        self.data['name'] = self.name
