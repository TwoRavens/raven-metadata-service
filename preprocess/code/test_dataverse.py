import glob
import subprocess

for file in glob.glob('../../test_data/dataverse/data/*'):
    filename = file.split('/')[-1]
    subprocess.run(f'python preprocess.py "{file}" "../../test_data/dataverse/python/{filename}"', shell=True)
