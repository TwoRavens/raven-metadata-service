"""
Simple test for celery to run preprocess tasks
"""
from __future__ import absolute_import, unicode_literals

import sys
from os.path import \
    (abspath, basename, dirname, isdir, isfile, join, splitext)

# Add preprocess code dir
PREPROCESS_DIR = join(dirname(dirname(dirname(abspath(__file__)))),
                      'preprocess',
                      'code')
sys.path.append(PREPROCESS_DIR)

from datetime import datetime
import time
from celery import Celery, shared_task
from ravens_metadata_apps.utils.random_util import get_alphanumeric_lowercase


from preprocess_runner import \
    (PreprocessRunner, ACCEPTABLE_EXT_LIST,
     CSV_FILE_EXT, TAB_FILE_EXT)
from msg_util import msg, msgt

from celery import task, shared_task

from ravens_metadata.celery import celery_app



@shared_task
def preprocess_csv_file(input_file, **kwargs):
    """Run preprocess on a selected file"""

    job_id = kwargs.get('job_id')

    start_time = time.time()
    print('(%s) Start preprocess: %s' % (start_time, input_file))

    # Split out the filename and extension
    # - check if it's a valid file type
    #
    fname_base, fname_ext = splitext(basename(input_file))
    fname_ext_check = fname_ext.lower()
    if fname_ext_check == TAB_FILE_EXT:
        runner, err_msg = PreprocessRunner.load_from_tabular_file(\
                                    input_file,
                                    job_id=job_id)
    elif fname_ext_check == CSV_FILE_EXT:
        runner, err_msg = PreprocessRunner.load_from_csv_file(input_file,
                                                              job_id=job_id)
    else:
        err_msg = ('We currently do not process this file type.'
                   ' Please use a file with one of the following'
                   ' extensions: %s') % \
                   (ACCEPTABLE_EXT_LIST,)


    if err_msg:
        print('(%s) FAILED: %s' % (input_file, err_msg))
        return dict(success=False,
                    input_file=input_file,
                    message=err_msg)

    elapsed_time = time.time() - start_time
    elapsed_time_str = time.strftime("%H:%M:%S", time.gmtime(elapsed_time))

    return dict(success=True,
                input_file=input_file,
                message="File processed.",
                elapsed_time=elapsed_time_str,
                data=runner.get_final_dict())
