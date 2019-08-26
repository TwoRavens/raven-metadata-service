import csv
import glob
import os
import subprocess

for file in glob.glob('../../test_data/dataverse/*/files.csv'):
    with open(file) as f:
        r = csv.reader(f)
        for row in r:
            if row and row[-2].split('.')[-1].lower() in 'csv tab tsv'.split():
                id = row[-1].split('&')[0].split('?')[-1]
                url = f'/api/access/datafile/:persistentId?{id}'
                id = id.split('/')[2]
                url = f'https://dataverse.{"unc" if "/sppq/" in file else "harvard"}.edu{url}'
                
                file = f'../../test_data/dataverse/data/{id}_{row[-2]}' 
                if os.path.isfile(file) or os.path.isfile(f'../../test_data/dataverse/changes/{id}_{row[-2]}'):
                    continue
                
                subprocess.run(f'wget -T 10 -O "{file}" {url}', shell=True)
