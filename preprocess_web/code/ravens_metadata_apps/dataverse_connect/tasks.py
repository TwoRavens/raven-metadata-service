import os, sys
import csv
from os.path import abspath, dirname, join

from msg_util import msg, msgt
from ravens_metadata_apps.dataverse_connect.dataverse_file_retriever import \
    (DataverseFileRetriever)
from ravens_metadata_apps.preprocess_jobs.job_util import JobUtil
from ravens_metadata_apps.utils.basic_response import \
    (ok_resp, err_resp, err_resp_with_data)
from ravens_metadata_apps.preprocess_jobs.tasks import preprocess_csv_file

from celery import task, shared_task
from celery.result import AsyncResult

@task
def preprocess_dataverse_file(dv_url, **kwargs):
    """Test task to download file and preprocess it
    kwargs: params to pass onto DataverseFileRetriever:
     - dataset_id - id of the dataset
     - preprocess_job - an instance of PreprocessJob
        - recommended if you plan to add a celery `task_id` to it
    """
    file_retriever = DataverseFileRetriever(dv_url, **kwargs)
    if file_retriever.has_error():
        print('error found: %s' % file_retriever.get_error_message())
        err_data = dict(dataverse_url=dv_url)
        return err_resp_with_data(file_retriever.get_error_message(), err_data)

    return JobUtil.start_preprocess(file_retriever.preprocess_job)
