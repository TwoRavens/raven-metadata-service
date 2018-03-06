"""
Quick hack of aiohttp + preprocess a queue
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
from collections import OrderedDict

from celery.result import AsyncResult

from random_util import get_alphanumeric_lowercase

from aiohttp import web
import aiohttp_jinja2, jinja2


from preprocess_runner import PreprocessRunner
from msg_util import msg, msgt
from response_util import get_ok_resp, get_err_resp
from basic_preprocess import preprocess_csv_file

UPLOAD_DEST_DIR = join(dirname(dirname(abspath(__file__))), 'uploaded_test_files')
if not isdir(UPLOAD_DEST_DIR):
    os.makedirs(UPLOAD_DEST_DIR)

TEMPLATE_DIR = join(dirname(abspath(__file__)), 'templates')



async def hello(request):
    """Test, health check"""
    name = request.match_info.get('name', "Anonymous")
    text = "Hello, " + name
    return web.Response(text=text)


@aiohttp_jinja2.template('upload_form.html')
async def show_upload_form(request):
    """upload form"""
    return {'title': 'upload test'}

async def get_progress(request):
    """given a celery task id, retrieve the state and posssibly the result"""

    task_id = request.match_info.get('task_id', None)
    if not task_id:
        return web.json_response(get_err_resp('please send a task_id'))


    ye_task = AsyncResult(task_id,
                          app=preprocess_csv_file)

    if ye_task.state == 'SUCCESS':
        return web.json_response(\
                get_ok_resp('looking good: %s' % (ye_task.result['input_file']),
                            data=ye_task.result['data']))

    return web.json_response(\
            get_ok_resp('state is: %s' % ye_task.state))


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

    accepted_files = ['.tab', '.csv']   # move this somewhere into code/preprocess
    if not fname_ext.lower() in accepted_files:
        user_msg = 'Sorry, the file type was not recognized. Accepted: %s' % accepted_files
        return web.json_response(get_err_resp(user_msg))

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

    ye_task = preprocess_csv_file.delay(upload_fname)

    if ye_task.ready():
        user_msg = 'DONE!! input_file: %s' % ye_task.result['input_file']
        return web.json_response(\
                    get_ok_resp(user_msg))
                                #data=runner.get_final_dict()))

    data_for_user = dict(task_id=ye_task.id,
                         task_state=ye_task.state)
    #import ipdb; ipdb.set_trace()
    user_msg = ('preprocess in process. progress url:'
                ' http://127.0.0.1:8080/progress/%s') % (ye_task.id)
    return web.json_response(\
                get_ok_resp(user_msg,
                            data=data_for_user),
                status=201)

#-------------------------------------------------
# Assign handlers
#-------------------------------------------------
app = web.Application()
aiohttp_jinja2.setup(app,
                     loader=jinja2.FileSystemLoader(TEMPLATE_DIR))

app.router.add_get('/upload-form', show_upload_form)
app.router.add_post('/upload', store_uploaded_file)
app.router.add_get('/progress/{task_id}', get_progress)

app.router.add_get('/{name}', hello)
app.router.add_get('/', hello)

web.run_app(app)
"""
import requests
url = 'http://127.0.0.1:8080/upload'
tfile = '/Users/ramanprasad/Documents/github-rp/raven-metadata-service/preprocess_service/test_input/fearonLaitin.tab'; files = {'data_file': open(tfile, 'rb')}; r = requests.post(url, files=files); r.text

tfile = '/Users/ramanprasad/Documents/github-rp/raven-metadata-service/preprocess_service/test_input/full1960.tab'; files = {'data_file': open(tfile, 'rb')}; r = requests.post(url, files=files); r.text
"""
