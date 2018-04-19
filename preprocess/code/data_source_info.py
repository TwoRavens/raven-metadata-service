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
        self.data = dict(type =self.type, format =self.format, name =self.name)
