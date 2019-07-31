import glob
import json
import subprocess
import sys

import dictdiffer

def get_path(filename, where='python'):
    return f'../../test_data/dataverse/{where}/{filename}'

def diff(filename, py_path, R_path):
    try:
        py_obj = json.load(open(py_path))
    except:
        py_obj = {}
    try:
        R_obj = json.load(open(R_path))
    except:
        R_obj = {}

    dif = list(dictdiffer.diff(R_obj, py_obj))
    if dif:
        with open(get_path(filename, 'changes'), 'w') as f:
            json.dump(dif, f, indent=2 )

for file in glob.glob('../../test_data/dataverse/data/*'):
    filename = file.split('/')[-1]
    py_path = get_path(filename)
    R_path = get_path(filename, 'R')
    if sys.argv[1] == 'diff':
        diff(filename, py_path, R_path)
        continue

    cmd = f'python preprocess.py "{file}" "{py_path}"'
    if sys.argv[1]:
        cmd = f'Rscript ../../rscripts/runPreprocess.R "{file}" ../../rscripts/'
    result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE)
    try:
        obj = json.loads(result.stdout.decode('utf8').split('---START-PREPROCESS-JSON---')[1].split('---END-PREPROCESS-JSON---')[0])
    except:
        continue 
    with open(R_path, 'w') as f:
        json.dump(obj, f) 
