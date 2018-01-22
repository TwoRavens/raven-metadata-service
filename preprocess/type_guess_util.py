import json
from collections import OrderedDict
from os.path import join, isfile, isdir

import numpy
import pandas as pd

from col_info_constants import *

class ColumnInfo(object):

    def __init__(self, numchar_val, interval, nature, binary, time_val):
        """Set column info values"""
        self.numchar = numchar_val
        self.interval = interval
        self.nature = nature
        self.binary = binary
        self.time_val = time_val


class TypeGuessUtil(object):
    """Check variable types of a dataframe"""

    def __init__(self, dataframe):
        """Init with a pandas dataframe"""
        assert dataframe is not None, "dataframe can't be None"

        self.df = dataframe
        self.check_types()


    def check_types(self):
        """check the types of the dataframe"""
        pass
        # iterate through variables and check...

def typeGuess(data):
    print ("data in typeGuess",data)
    k=len(data.columns)
    print ("column count:",k)

    out=list(varnameTypes=data.columns)
    print ("my out:",out)

    def check_decimal(x):
        """Check if variable is a decimal"""
        result = False
        level = numpy.math.floor(x)
        if any(x!=level):
            result=True;

        return result;

    def nature(x,c,nat):
        if (c):
            if(all(x>=0 & x<=1)):
                return nat[5]
            elif(all(x >=0 & x <=100) & min(x) < 15 & max(x) > 85):
                return nat[5] ;
            else:
                return nat[4];

        else:
            return nat[2];


    def time(x):
        return "no";



    return;
