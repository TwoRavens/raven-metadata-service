import glob
import json
import subprocess
import sys

for file in glob.glob('../../test_data/dataverse/data/*'):
    filename = file.split('/')[-1]
    cmd = f'python preprocess.py "{file}" "../../test_data/dataverse/python/{filename}"'
    if sys.argv[1]:
        cmd = f'Rscript ../../rscripts/runPreprocess.R "{file}" ../../rscripts/'
    result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE)
    try:
        obj = json.loads(result.stdout.decode('utf8').split('---START-PREPROCESS-JSON---')[1].split('---END-PREPROCESS-JSON---')[0])
    except:
        continue 
    with open(f'../../test_data/dataverse/R/{filename}', 'w') as f:
        json.dump(obj, f) 
