import json
from collections import OrderedDict
from os.path import join, isfile, isdir

import numpy
import pandas as pd
from col_info_constants import *


class ColumnInfo(object):

    def __init__(self, numchar_val, interval, nature, binary, time_val):
        """Set column info values"""
        self.numchar_val = numchar_val
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
        self.colcount = len(self.df.columns)
        self.check_types()


    def check_types(self):
        """check the types of the dataframe"""
        pass
        # iterate through variables and check...

    def typeGuess(data):
        print ("data in typeGuess", data)
        k= len(data.columns)
        print ("column count:", k)
        print("my out:", out)
        out= OrderedDict()


        def check_decimal(x):
            """Check if variable is a decimal"""
            result = False
            level = numpy.math.floor(x)
            if any(x!= level):
                result= True

            return result

        def check_nature(x, c, nat):
            if c:
                if all(x >= 0 & x <= 1) :
                    return nat[5]
                elif all(x >= 0 & x <= 100) & min(x) < 15 & max(x) > 85 :
                    return nat[5]
                else:
                    return nat[4]

            else:
                return nat[2]


        def check_time(x):
            return "no"

        def isfactor(x):
            pass

        def islogical(x):
            if(type(x) == type(True)):
                return True
            else:
                return False
        for i in range(k):
            """looping the column and adding to the dict"""
            """Sample 'out' from preprocess.R :
                    $varnamesTypes
                    [1] "ccode.country.cname.cmark.year.wars.war.warl.onset.ethonset.durest.aim.casename.ended.ethwar.waryrs.pop.lpop.polity2.gdpen.gdptype.gdpenl.lgdpenl1.lpopl1.region.western.eeurop.lamerica.ssafrica.asia.nafrme.colbrit.colfra.mtnest.lmtnest.elevdiff.Oil.ncontig.ethfrac.ef.plural.second.numlang.relfrac.plurrel.minrelpc.muslim.nwstate.polity2l.instab.anocl.deml.empethfrac.empwarl.emponset.empgdpenl.emplpopl.emplmtnest.empncontig.empolity2l.sdwars.sdonset.colwars.colonset.cowwars.cowonset.cowwarl.sdwarl.colwarl"

                    $defaultInterval
                    [1] "discrete"

                    $defaultNumchar
                    [1] "character"

                    $defaultNature
                    [1] "nominal"

                    $defaultBinary
                    [1] "no"

                    $defaultTime
                    [1] "no"

                 """
            var = data[ : i]

            out['defaultTime'] = check_time(var)
            if(isfactor(var) | islogical(var)):
                out['defaultInterval']= ColumnInfo.interval[2]
                out['defaultNumchar'] = ColumnInfo.numchar_val[2]
                out['defaultNature'] = ColumnInfo.nature[1]
                var=str(var)
                var.dropna() #to remove the rows with NA
                var = int(var)
                if(len(series.unique(var))==2):
                    out['defaultBinary']= ColumnInfo.binary[1]

                if any(pd.isnull(var)):
                    out['defaultInterval'] = ColumnInfo.interval[2]
                    out['defaultNumchar'] = ColumnInfo.numchar_val[2]
                    out['defaultNature'] = ColumnInfo.nature[1]
                else:
                    out['defaultNumchar'] = ColumnInfo.numchar_val[1]

                    decimal= check_decimal(var)
                    if(decimal):
                        out['defaultInterval'] = ColumnInfo.interval[1]
                        out['defaultNature'] = check_nature(var,True,ColumnInfo.nature)
                    else:
                        out['defaultInterval'] = ColumnInfo.interval[2]
                        out['defaultNature'] = check_nature(var, False, ColumnInfo.nature)



        return out
