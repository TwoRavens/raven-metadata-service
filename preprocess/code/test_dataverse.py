import glob
import json
import subprocess
import sys

import dictdiffer

from preprocess_runner import PreprocessRunner

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

    changes = [] 
    for change in list(dictdiffer.diff(R_obj, py_obj, ignore='self dataset variableDisplay'.split(), tolerance=0.01)):
        if change[0] != 'change' or change[2] not in [('yes', True), ('no', False), ('no', 'unknown')]:
            changes.append(change)

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

