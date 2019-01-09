"""
Simple test for celery to run preprocess tasks
"""
from datetime import datetime
import time

from celery import task, shared_task

from ravens_metadata_apps.preprocess_jobs.models import \
    (PreprocessJob,
     STATE_SUCCESS, STATE_FAILURE)
from ravens_metadata_apps.utils.basic_response import \
    (ok_resp, err_resp)
from ravens_metadata_apps.r_preprocess.preprocess_util import PreprocessUtil

from msg_util import msg, msgt

from ravens_metadata.celery import celery_app


@shared_task
def run_r_preprocess_file(job_id, **kwargs):
    """Run preprocess on a selected file"""
    if not job_id:
        return err_resp('Not job_id specified in run_r_preprocess_file')

    putil = PreprocessUtil(job_id)
    if putil.has_error():
        return err_resp(putil.get_error_message())
    else:
        return ok_resp('all set!')
