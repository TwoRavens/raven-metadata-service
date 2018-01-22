import json
from collections import OrderedDict
from os.path import join, isfile, isdir


import numpy
import pandas as pd


class MyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, numpy.integer):
            return int(obj)
        elif isinstance(obj, numpy.floating):
            return float(obj)
        elif isinstance(obj, numpy.ndarray):
            return obj.tolist()
        else:
            return super(MyEncoder, self).default(obj)

# if file input valid
def test_run(input_file):
    assert isfile(input_file), 'file not found: %s' % input_file


    df = pd.read_csv(input_file)


    typeGuess(df)
    variables = dict()
    colnames = list(df.columns)
    for colname in colnames:
        od = OrderedDict()
        od['labl'] = ''
        od['varnamesSumStat'] = colname
        od['median'] = df[colname].median()
        # mode
        #od['mode'] = df[colname].mode()[0]

        od['mean'] = df[colname].mean()
        od['max'] = df[colname].max()
        od['min'] = df[colname].min()

        od['invalid'] = df[colname].isnull().sum()
        od['valid'] = df[colname].count()

        od['sd'] = df[colname].std()
        od['uniques'] = df[colname].nunique()

        # NEED TO ADD herfindahl
        #col_total = float(df[colname].sum())
        #hhi_elements = [(float(val)/col_total)**2
        #                for val in list(df[colname].values)]

        #od['herfindahl'] = sum(hhi_elements)
        od['herfindahl'] = '?'

        if od['uniques']:
            freq_cnt = None
            mid_pt = int(od['uniques'] / 2)

            for idx, freq_cnt in enumerate(df[colname].value_counts().iteritems(), 1):
                if idx == 1:
                    od['mode'], od['mode_freq'] = freq_cnt
                if idx == mid_pt:
                    od['mid'], od['mid_freq'] = freq_cnt

            od['fewest'], od['fewest_freq'] = freq_cnt

        # convert R typeGuess function

        #import ipdb; ipdb.set_trace()
        #df["weight"].mean()
        """
        "herfindahl":0.0265753794874105,

        "mid":"199",
        "freqmid":"2",
        "numchar":"numeric",
        "nature":"ratio",
        "binary":"no",
        "interval":"continuous",
        "time":"no",
        "varnamesTypes":"displacement",
        "defaultInterval":"continuous",
        "defaultNumchar":"numeric",
        "defaultNature":"ratio",
        "defaultBinary":"no",
        "defaultTime":"no"
        """
        variables[colname] = od

    print(json.dumps(variables, indent=4, cls=MyEncoder))


    #print (df)
    """
    "d3mIndex":{
 "labl":"",
 "varnamesSumStat":"d3mIndex",
 "median":202.5,
 "mean":200.647651006711,
 "mode":"1",
 "max":397,
 "min":1,
 "invalid":0,
 "valid":298,
 "sd":111.681244387762,
 "uniques":298,
 "herfindahl":0.00335570469798658,
 "freqmode":1,
 "fewest":"1",
 "mid":"1",
 "freqfewest":"1",
 "freqmid":"1",
 "numchar":"numeric",
 "nature":"ordinal",
 "binary":"no",
 "interval":"discrete",
 "time":"no",
 "varnamesTypes":"d3mIndex",
 "defaultInterval":"discrete",
 "defaultNumchar":"numeric",
 "defaultNature":"ordinal",
 "defaultBinary":"no",
 "defaultTime":"no"
 """
def typeGuess(data):
    print("data in typeGuess",data)
    k=len(data.columns)
    print("column count:",k)

    out=list(varnameTypes=data.columns)
    print("my out:",out)

    def decimal(x):
        result=False
        level= numpy.math.floor(x)
        if any(x!=level): result=True;
        return  result;

    def nature(x,c,nat):
        if (c):
            if(all(x>=0 & x<=1)):return nat[5];
            elif(all(x >=0 & x <=100) & min(x) < 15 & max(x) > 85) : return nat[5] ;
            else: return nat[4];
        else: return nat[2];


    def time(x):
        return "no";



    return;

if __name__ == '__main__':
    input_file = join('input', 'learningData.csv')
    test_run(input_file)



#To do list for preprocess.R -> preprocess.py
#1.Input from different sources
#2.function typeGuess()
#3.