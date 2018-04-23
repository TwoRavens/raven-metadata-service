"""
Simple test for celery to run preprocess tasks
"""
from __future__ import absolute_import, unicode_literals

import json
from django.utils import timezone
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
from django.core.files.base import ContentFile

from celery import task, shared_task
from celery.result import AsyncResult

from ravens_metadata_apps.utils.random_util import get_alphanumeric_lowercase
from ravens_metadata_apps.preprocess_jobs.preprocess_result_updater import \
    (PreprocessResultUpdater)
from ravens_metadata_apps.preprocess_jobs.models import \
    (PreprocessJob,
     STATE_SUCCESS, STATE_FAILURE)
from ravens_metadata_apps.utils.basic_response import \
    (ok_resp, err_resp)
from preprocess_runner import \
    (PreprocessRunner, ACCEPTABLE_EXT_LIST,
     CSV_FILE_EXT, TAB_FILE_EXT)
from msg_util import msg, msgt

from ravens_metadata.celery import celery_app


@shared_task
def preprocess_csv_file(input_file, **kwargs):
    """Run preprocess on a selected file"""
    job_id = kwargs.get('job_id')

    start_time = time.time()
    print('(%s) Start preprocess: %s' % (start_time, input_file))

    fname = basename(input_file)
    print("*************fname : ", fname)
    fname_base, fname_ext = splitext(fname)


    # Split out the filename and extension
    # - check if it's a valid file type
    #
    # fname_base, fname_ext = splitext(basename(input_file))
    # fname_ext_check = fname_ext.lower()
    # if fname_ext_check == TAB_FILE_EXT:
    #     runner, err_msg = PreprocessRunner.load_from_tabular_file(\
    #                                 input_file,
    #                                 job_id=job_id)
    # elif fname_ext_check == CSV_FILE_EXT:
    #     runner, err_msg = PreprocessRunner.load_from_csv_file(input_file,
    #                                                           job_id=job_id)

    runner, err_msg = PreprocessRunner.load_from_file( \
                                            input_file,
                                    job_id=job_id,
                                    fname = fname, fname_base = fname_base,fname_ext = fname_ext) # only input_file and job_id should be sent.


    if err_msg:

        print('(%s) FAILED: %s' % (input_file, err_msg))
        result_info = dict(success=False,
                           job_id=job_id,
                           input_file=input_file,
                           user_message=err_msg)
    else:
        elapsed_time = time.time() - start_time
        elapsed_time_str = time.strftime("%H:%M:%S", time.gmtime(elapsed_time))

        result_info = dict(success=True,
                           job_id=job_id,
                           input_file=input_file,
                           user_message="File processed.",
                           elapsed_time=elapsed_time_str,
                           data=runner.get_final_dict())

    updater = PreprocessResultUpdater(**result_info)

    if updater.has_error:
        return err_resp(updater.error_message)

    return ok_resp('All set')


def check_job_status_by_id(job_id):
    """Check/update the job status by job_id"""
    print('=' * 40)
    print('check_status_by_job_id', job_id)
    print('=' * 40)

    it_worked = check_job_status(job)
    if it_worked:
        return ok_resp(job)

    user_msg = ('PreprocessJob still in process: %s') % (job_id)
    return err_resp(user_msg)



def check_job_status(job):
    """Check/update the job status"""
    assert isinstance(job, PreprocessJob),\
           'job must be a PreprocessJob'

    if job.is_finished():
        return True

    return True
    """
    ye_task = AsyncResult(job.task_id,
                          app=preprocess_csv_file)

    if ye_task.state == 'SUCCESS':

        if ye_task.result['success']:

            preprocess_data = ContentFile(json.dumps(ye_task.result['data']))

            new_name = 'preprocess_%s.json' % get_alphanumeric_lowercase(8)
            job.preprocess_file.save(new_name,
                                     preprocess_data)
            job.set_state_success()

            job.user_message = 'Task completed!  Preprocess is available'
            job.save()

        else:
            # Didn't work so well
            job.set_state_failure(ye_task.result['message'])
            job.save()

        ye_task.forget()
        return True

    elif ye_task.state == STATE_FAILURE:
        job.set_state_failure('ye_task failed....')
        job.save()
        ye_task.forget()
        return True

    return False
    """
