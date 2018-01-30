from collections import OrderedDict
import json
from col_info_constants import *

class ColumnInfo(object):

    def __init__(self, colname):
        """Init with column name"""
        # -------------
        # more general
        # -------------
        self.colname = colname
        self.valid=None
        self.invalid=None

        # ----------------------
        # Type Guess Info
        # ----------------------
        self.numchar_val = None
        self.default_interval = None
        self.nature = None
        self.time_val = None
        self.binary = None

        # set at type util
        self.varnamesSumStat = None

        # Stats Info
        self.mode = None
        self.freqmode = None
        self.mid = None
        self.fewest = None
        self.freqmid = None
        self.freqfewest = None
        self.median = None
        self.mean = None
        self.max = None
        self.min = None
        self.sd = None
        self.herfindahl = None

        """
          out<-list(varnamesSumStat=colnames(data), median=as.vector(rep(NA,length.out=k)), mean=as.vector(rep(NA,length.out=k)), mode=as.vector(rep(NA,length.out=k)), max=as.vector(rep(NA,length.out=k)), min=as.vector(rep(NA,length.out=k)), invalid=as.vector(rep(NA,length.out=k)), valid=as.vector(rep(NA,length.out=k)), sd=as.vector(rep(NA,length.out=k)), uniques=as.vector(rep(NA,length.out=k)), herfindahl=as.vector(rep(NA,length.out=k)), freqmode=as.vector(rep(NA,length.out=k)), fewest=as.vector(rep(NA,length.out=k)), mid=as.vector(rep(NA,length.out=k)), freqfewest=as.vector(rep(NA,length.out=k)), freqmid=as.vector(rep(NA,length.out=k)) )
         """


    def is_numeric(self):
        # is this NUMCHAR_NUMERIC?
        return self.numchar_val == NUMCHAR_NUMERIC

    def is_character(self):
        # is this NUMCHAR_CHARACTER?
        return self.numchar_val == NUMCHAR_CHARACTER



    def get_variable_labels(self):
        """Set labels for variable output"""
        label_list = (
            ('varnameTypes', self.colname),
            ('defaultInterval', self.default_interval),
            ('defaultNumchar', self.numchar_val),
            ('defaultNature', self.nature),
            ('defaultBinary', self.binary),
            ('defaultTime', self.time_val),
            )

        return label_list

    def as_dict(self, as_string=False):
        """For final output"""
        od = OrderedDict()

        for label, val in self.get_variable_labels():
            od[label] = val

        if as_string:
            return json.dumps(od)

        return od
