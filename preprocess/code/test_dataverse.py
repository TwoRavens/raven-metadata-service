import glob
import json
import subprocess
import sys

import dictdiffer
import pandas as pd 

from preprocess_runner import PreprocessRunner

def get_path(filename, where='python'):
    return f'../../test_data/dataverse/{where}/{filename}'

replace = dict(
    binary = 'defaultBinary',
    cdfPlotType = 'cdfplottype',
    cdfPlotX = 'cdfplotx',
    cdfPlotY = 'cdfploty',
    description = 'labl', 
    fewestFreq = 'freqfewest',
    fewestValues = 'fewest',
    herfindahlIndex = 'herfindahl',
    interval = 'defaultInterval',
    invalidCount = 'invalid',
    max = 'max',
    mean = 'mean',
    median = 'median',
    midpoint = 'mid',
    midpointFreq = 'freqmid',
    min = 'min',
    mode = 'mode',
    modeFreq = 'freqmode',
    nature = 'defaultNature',
    numchar = 'defaultNumchar',
    pdfPlotType = 'plottype',
    pdfPlotX = 'plotx',
    pdfPlotY = 'ploty',
    stdDev = 'sd',
    time = 'defaultTime',
    validCount = 'valid', 
    variableName = 'varnamesSumStat',
    uniqueCount = 'uniques'
)

ignore = 'cdfPlotType cdfPlotX cdfPlotY fewestFreq fewestValues herfindahlIndex midpoint midpointFreq mode pdfPlotType pdfPlotX pdfPlotY plotValues'.split()
ignore += ['invalidCount', 'validCount', 'uniqueCount'] # differ in missingness

def diff(filename, py_path, R_path):
    try:
        py_obj = json.load(open(py_path))
        for var in py_obj.get('variables', []):
            for (k, k1) in replace.items():
                if k1 in ('cdfplotx', 'cdfploty', 'plotx', 'ploty'):
                    val = py_obj['variables'][var].get(k)
                    if isinstance(val, list): 
                        py_obj['variables'][var][k] = sorted(val)

            for k in ignore:
                try:
                    del py_obj['variables'][var][k]
                except:
                    pass
    except:
        py_obj = {}

    try:
        R_obj = json.load(open(R_path))
    except:
        R_obj = {} 

    R_obj1 = dict(variables={})
    for var in R_obj.get('variables', []):
        R_obj1['variables'][var] = {} 
        for (k, k1) in replace.items():
            val = R_obj['variables'][var].get(k1)
            if val == 0.0 and k == 'modeFreq' or val =='NULL':
                val = None

            try:
                val = float(val)
            except:
                pass

            #if k1 in ('cdfplotx', 'cdfploty', 'plotx', 'ploty') and isinstance(val, list): 
            #    R_obj1['variables'][var][k] = []#sorted(val) 
            if k not in ignore:
                R_obj1['variables'][var][k] = val

    changes = [] 
    for change in list(dictdiffer.diff(R_obj1, py_obj, ignore='self dataset variableDisplay'.split(), tolerance=0.01)):
        if change[0] == 'change' and change[2] not in [('yes', True), ('no', False), ('no', 'unknown')]:
            if not (change[2][0] == 'NA' and pd.isna(change[2][1])):
                changes.append(change)

    if changes:
        with open(get_path(filename, 'changes'), 'w') as f:
            json.dump(changes, f, indent=2)

errs = {}
for file in glob.glob('../../test_data/dataverse/data/*'):
    filename = file.split('/')[-1]
    py_path = get_path(filename)
    R_path = get_path(filename, 'R')

    if sys.argv[1] == 'diff':
        diff(filename, py_path, R_path)
        continue

    if sys.argv[1] == 'py':
        runner, err_msg = PreprocessRunner.load_from_file(file)
        if err_msg:
            errs[filename] = err_msg
            continue

        jstring = runner.get_final_json(indent=4)
        open(py_path, 'w').write(jstring)
        continue

    cmd = f'Rscript ../../rscripts/runPreprocess.R "{file}" ../../rscripts/'
    result = subprocess.run(cmd, check=True, shell=True, stdout=subprocess.PIPE)
    print(result.stdout.decode('utf8'))
    obj = json.loads(result.stdout.decode('utf8').split('---START-PREPROCESS-JSON---')[1].split('---END-PREPROCESS-JSON---')[0])

    with open(R_path, 'w') as f:
        json.dump(obj, f) 

with open(get_path('errors.json'), 'w') as f:
    json.dump(errs, f, indent=2) 

