"""
Simple test for celery to run preprocess tasks
"""
import sys
import os
from os.path import \
    (abspath, basename, dirname, isdir, isfile, join, splitext)
# Add preprocess code dir
PREPROCESS_DIR = join(dirname(dirname(dirname(abspath(__file__)))),
                      'preprocess',
                      'code')
sys.path.append(PREPROCESS_DIR)
# Add preprocess code dir
PREPROCESS_SVC_DIR = join(dirname(dirname(dirname(abspath(__file__)))),
                          'preprocess_service',
                          'code')
sys.path.append(PREPROCESS_SVC_DIR)
for x in sys.path: print(x)

from datetime import datetime
import time
import json
import logging

#from celery import Celery
from random_util import get_alphanumeric_lowercase

from aiohttp import web


from preprocess_runner import PreprocessRunner
from msg_util import msg, msgt
from response_util import get_ok_resp, get_err_resp

UPLOAD_DEST_DIR = join(dirname(dirname(abspath(__file__))), 'uploaded_test_files')
if not isdir(UPLOAD_DEST_DIR):
    os.makedirs(UPLOAD_DEST_DIR)


async def hello(request):
    """Test, health check"""
    name = request.match_info.get('name', "Anonymous")
    text = "Hello, " + name
    return web.Response(text=text)

async def store_uploaded_file(request):
    """File upload test
    ref: https://docs.aiohttp.org/en/stable/web_quickstart.html#file-uploads

    Handled as a form sent via POST,
        attribute "data_file" contains the file content
    """
    #-------------------------------------------------
    # Upload file
    #-------------------------------------------------
    try:
        reader = await request.multipart()
    except AssertionError as err_obj:
        user_msg = 'Failed to process POST as a multipart form: %s' % err_obj
        return web.json_response(get_err_resp(user_msg))

    field = await reader.next()
    assert field.name == 'data_file'
    filename = field.filename

    fname_base, fname_ext = splitext(basename(filename))

    new_fname = '%s_%s%s' % (fname_base,
                             get_alphanumeric_lowercase(5),
                             fname_ext)

    upload_fname = join(UPLOAD_DEST_DIR, new_fname)

    # You cannot rely on Content-Length if transfer is chunked.
    size = 0
    with open(upload_fname, 'wb') as f:
        while True:
            chunk = await field.read_chunk()  # 8192 bytes by default.
            if not chunk:
                break
            size += len(chunk)
            f.write(chunk)


    #-------------------------------------------------
    # Run preprocess
    #-------------------------------------------------
    accepted_files = ['.tab', '.csv']   # move this somewhere into code/preprocess
    if upload_fname.lower().endswith('.tab'):
        runner, preprocess_err_msg = PreprocessRunner.load_from_tabular_file(upload_fname)
    elif upload_fname.lower().endswith('.csv'):
        runner, preprocess_err_msg = PreprocessRunner.load_from_csv_file(upload_fname)
    else:
        user_msg = 'Sorry, the file type was not recognized. Accepted: %s' % accepted_files
        return web.json_response(get_err_resp(user_msg))

    if preprocess_err_msg:
        return web.json_response(get_err_resp(preprocess_err_msg))

    #runner.show_final_info()

    jstring = runner.get_final_json(indent=None)
    #msg(jstring)

    return web.json_response(\
                get_ok_resp('preprocess worked',
                            data=jstring))
                            #data=runner.get_final_dict()))

    return web.Response(text='{} sized of {} successfully stored'
                             ''.format(upload_fname, size))

#-------------------------------------------------
# Assign handlers
#-------------------------------------------------
app = web.Application()
app.router.add_post('/upload', store_uploaded_file)
app.router.add_get('/{name}', hello)
app.router.add_get('/', hello)

web.run_app(app)


"""
import requests
url = 'http://127.0.0.1:8080/upload'
tfile = '/Users/ramanprasad/Documents/github-rp/raven-metadata-service/preprocess/input/test_file_01.csv'; files = {'data_file': open(tfile, 'rb')}; r = requests.post(url, files=files); r.text

"""
