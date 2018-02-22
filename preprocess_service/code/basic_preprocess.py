import time
import json
from os.path import isdir, isfile

import xlrd
import pandas as pd
from celery import Celery

BROKER_URL = 'redis://localhost'

app = Celery('basic_preprocess',
             backend=BROKER_URL,
             broker=BROKER_URL)


@app.task
def preprocess_csv_file(fname):
    """Run preprocess on a csv file"""
    if not isfile(fname):
        return False, 'Not a file'

    try:
        xl_workbook = xlrd.open_workbook(fname)
    except Exception as ex_obj:
        return False, 'XLRD failed to open file: %s' % ex_obj

    df = None
    try:
        df = pd.read_excel(fname)
    except Exception as ex_obj:
        return False, 'Pandas failed to open file: %s' % ex_obj

    return True, 'It works! %s' % df.columns


"""
python
import os
from os.path import isfile, isdir, join
import time
from tasks import read_dv_xls

file_dir = '/Users/rmp553/Documents/iqss-git/dataverse-helper-scripts/src/file_downloader/output/output_2016-0427'

r = read_dv_xls.delay('/Users/rmp553/Documents/iqss-git/dataverse-helper-scripts/src/file_downloader/output/output_2016-0427/0101351/Raw Data Codebook.xls')

import os

task_items = []
cnt = 0
for item in os.listdir(file_dir):
    full_path = join(file_dir, item)
    if isdir(full_path):
        fnames = os.listdir(full_path)
        fnames = [x for x in fnames if x.lower().endswith('.xls')]
        for xls_name in fnames:
            #if cnt >= 500:
            #    continue
            cnt +=1
            full_xls_name = join(full_path, xls_name)
            print ('%d) add task: %s' % (cnt, full_xls_name))
            r = read_dv_xls.delay(full_xls_name)
            task_items.append(r)

time.sleep(5)
cnt = 0
for t in task_items:
    cnt += 1
    if t.ready():
        print (cnt, t.result)
    else:
        print (cnt, 'not ready')


"""
