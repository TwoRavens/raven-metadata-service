from collections import OrderedDict
import json

class ColumnInfo(object):
    def __init__(self, colname):
        """Init with column name"""
        self.colname = colname

        # default to None
        self.numchar_val = None
        self.default_interval = None
        self.nature = None
        self.binary = None
        self.time_val = None

    def get_dict(self, as_string=False):
        """For final output"""
        od = OrderedDict()
        od['varnameTypes'] = self.colname
        # etc....

        if as_string:
            return json.dumps(od)

        return od
