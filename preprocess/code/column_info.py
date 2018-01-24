from collections import OrderedDict
import json
from col_info_constants import *

class ColumnInfo(object):

    def __init__(self, colname):
        """Init with column name"""
        self.colname = colname

        # ----------------------
        # Type Guess Info
        # ----------------------
        self.numchar_val = None
        self.default_interval = None
        self.nature = None
        self.time_val = None
        self.binary = None

        # Stats Info
        self.varnamesSumStat = None
        """
          out<-list(varnamesSumStat=colnames(data), median=as.vector(rep(NA,length.out=k)), mean=as.vector(rep(NA,length.out=k)), mode=as.vector(rep(NA,length.out=k)), max=as.vector(rep(NA,length.out=k)), min=as.vector(rep(NA,length.out=k)), invalid=as.vector(rep(NA,length.out=k)), valid=as.vector(rep(NA,length.out=k)), sd=as.vector(rep(NA,length.out=k)), uniques=as.vector(rep(NA,length.out=k)), herfindahl=as.vector(rep(NA,length.out=k)), freqmode=as.vector(rep(NA,length.out=k)), fewest=as.vector(rep(NA,length.out=k)), mid=as.vector(rep(NA,length.out=k)), freqfewest=as.vector(rep(NA,length.out=k)), freqmid=as.vector(rep(NA,length.out=k)) )
         """


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
