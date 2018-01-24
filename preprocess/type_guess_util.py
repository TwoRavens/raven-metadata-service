import json
from collections import OrderedDict
from os.path import join, isfile, isdir
import random
import numpy as np
import pandas as pd

from col_info_constants import *
from column_info import *

class TypeGuessUtil(object):
    """Check variable types of a dataframe"""
    def __init__(self, dataframe):
        """Init with a pandas dataframe"""
        assert dataframe is not None, "dataframe can't be None"

        self.dataframe = dataframe
        self.colnames = self.dataframe.columns
        self.colcount = len(self.dataframe.columns)
        # print("data frame")
        # print(self.dataframe)
        # print("colnames")
        # print(self.colnames)
        # final output
        self.columnInfo_dict={}
        # # final outout returned
        self.columnInfo_dict=self.check_types()


    def check_types(self):
        """check the types of the dataframe"""
        #print(self.colnames)
        #assert self.colnames, 'self.colnames must have values'
        self.colname=None
        self.numchar_val = None
        self.default_interval = None
        self.nature = None
        self.time_val = None
        self.binary = None
        variable_dict = dict()

        # Iterate though variables and set type info
        for colname in self.colnames:
            self.col_info = OrderedDict()
            self.colname=colname
            # print(colname)
            data_info= self.dataframe[colname]
            # print("data_info")
            # print(data_info)
            # print(type(data_info))
            # set time
            self.time_val = self.check_time(data_info)
            print("time_val")
            print(self.time_val)
            # set vals if factor or logical
            #

            print("******")
            if self.is_factor(data_info) or \
                self.is_logical(data_info):

                self.numchar_val = NUMCHAR_CHARACTER
                self.default_interval = INTERVAL_DISCRETE
                self.nature = NATURE_NOMINAL
                print("** column info data**")
                print(self.numchar_val)
                print(self.default_interval)
                print(self.nature)

                data_info.dropna(inplace=True)
                if (len(data_info.unique()) == 2):
                    print("#2")
                    self.binary= BINARY_NO
                    print(self.binary)
                    next()

            data_info.dropna(inplace=True)

            data_info=data_info.astype('int')
            # print(data_info)

            if (len(data_info.unique()) == 2):
                self.binary = BINARY_NO

            if any(data_info.isnull()):
                self.numchar_val = NUMCHAR_CHARACTER
                self.nature = NATURE_NOMINAL
                self.default_interval = INTERVAL_DISCRETE
                print("#3")
                print(self.numchar_val)
                print(self.default_interval)
                print(self.nature)
            else:
                self.numchar_val = NUMCHAR_NUMERIC
                print("#4")
                print(self.numchar_val)

                decimal = self.check_decimal(data_info)
                if(decimal):
                    self.col_info.default_interval = INTERVAL_CONTINUOUS
                    self.nature = self.check_nature(data_info, True, NATURE_VALUES)
                    print("#5")
                    print(self.nature)
                else:
                    self.default_interval = INTERVAL_DISCRETE
                    self.nature = self.check_nature(data_info, False, NATURE_VALUES)
                    print("#6")
                    print(self.nature)


            # some other stuff, dropna
           # ColumnInfo(col_info)
                    self.col_info['varnameTypes']= self.colname
                    self.col_info['defaultNumchar']= self.numchar_val
                    self.col_info['defaultInterval'] = self.default_interval
                    self.col_info['defaultNature'] = self.nature
                    self.col_info['defaultBinary'] = self.binary
                    self.col_info['defaultTime'] = self.time_val

            # print(self.col_info)
            variable_dict[colname] = self.col_info
            # print(variable_dict)
            continue  # go to next variable


            #print(colname)
        # print()
        print(json.dumps(variable_dict, indent=4))
        return variable_dict

    def is_factor(self, var_series):
        """Check if pandas Series is a factor"""
        return random.choice([True, False])

    def is_logical(self, var_series):
        """Check if pandas Series is a boolean"""
        return random.choice([True, False])

    def check_decimal(self,x):
        """Check if variable is a decimal"""
        result = False
        level = np.floor(x)
        if any(x != level):
            result = True

        return result

    def check_nature(self,x, c, nat):
        if c:
            if all(x >= 0 & x <= 1):
                return nat[5]
            elif all(x >= 0 & x <= 100) & min(x) < 15 & max(x) > 85:
                return nat[5]
            else:
                return nat[4]

        else:
            return nat[2]

    def check_time(self,data_info):
        return "no"


















    # def typeGuess(data):
    #     print ("data in typeGuess", data)
    #     k= len(data.columns)
    #     print ("column count:", k)
    #     print("my out:", out)
    #     out= OrderedDict()
    #
    #
    #
    #
    #     def islogical(x):
    #         if(type(x) == type(True)):
    #             return True
    #         else:
    #             return False
    #     for i in range(k):
    #         """looping the column and adding to the dict"""
    #         """Sample 'out' from preprocess.R :
    #                 $varnamesTypes
    #                 [1] "ccode.country.cname.cmark.year.wars.war.warl.onset.ethonset.durest.aim.casename.ended.ethwar.waryrs.pop.lpop.polity2.gdpen.gdptype.gdpenl.lgdpenl1.lpopl1.region.western.eeurop.lamerica.ssafrica.asia.nafrme.colbrit.colfra.mtnest.lmtnest.elevdiff.Oil.ncontig.ethfrac.ef.plural.second.numlang.relfrac.plurrel.minrelpc.muslim.nwstate.polity2l.instab.anocl.deml.empethfrac.empwarl.emponset.empgdpenl.emplpopl.emplmtnest.empncontig.empolity2l.sdwars.sdonset.colwars.colonset.cowwars.cowonset.cowwarl.sdwarl.colwarl"
    #
    #                 $defaultInterval
    #                 [1] "discrete"
    #
    #                 $defaultNumchar
    #                 [1] "character"
    #
    #                 $defaultNature
    #                 [1] "nominal"
    #
    #                 $defaultBinary
    #                 [1] "no"
    #
    #                 $defaultTime
    #                 [1] "no"
    #
    #              """
    #         var = data[ : i]
    #
    #         out['defaultTime'] = check_time(var)
    #         if(isfactor(var) | islogical(var)):
    #             out['defaultInterval']= colname.interval[2]
    #             out['defaultNumchar'] = colname.numchar_val[2]
    #             out['defaultNature'] = colname.nature[1]
    #             var=str(var)
    #             var.dropna() #to remove the rows with NA
    #             var = int(var)
    #             if(len(series.unique(var))==2):
    #                 out['defaultBinary']= colname.binary[1]
    #
    #             if any(pd.isnull(var)):
    #                 out['defaultInterval'] = colname.interval[2]
    #                 out['defaultNumchar'] = colname.numchar_val[2]
    #                 out['defaultNature'] = colname.nature[1]
    #             else:
    #                 out['defaultNumchar'] = colname.numchar_val[1]
    #
    #                 decimal= check_decimal(var)
    #                 if(decimal):
    #                     out['defaultInterval'] = colname.interval[1]
    #                     out['defaultNature'] = check_nature(var,True,colname.nature)
    #                 else:
    #                     out['defaultInterval'] = colname.interval[2]
    #                     out['defaultNature'] = check_nature(var, False, colname.nature)
    #
    #
    #
    #     return out
