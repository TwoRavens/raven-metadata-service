from collections import OrderedDict
import json
from col_info_constants import *

class ColumnInfo(object):
    def __init__(self, colname):
        """Init with column name"""


        self.colname = colname

        # default to None
        self.numchar_val = None
        self.default_interval = None
        self.nature = None
        self.time_val = None
        self.binary = None

    def is_numeric(self):
        # is this NUMCHAR_NUMERIC?
        return self.numchar_val == NUMCHAR_NUMERIC

    def as_dict(self, as_string=False):
        """For final output"""
        od = OrderedDict()
        od['varnameTypes'] = self.colname
        od['defaultInterval']= self.default_interval
        od['defaultNumchar'] = self.numchar_val
        od['defaultNature'] = self.nature
        od['defaultBinary'] = self.binary
        od['defaultTime'] = self.time_val


        if as_string:
            return json.dumps(od)

        return od
