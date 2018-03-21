"""Utility class for the preprocess workflow"""
import json, uuid
import pandas as pd
from datetime import datetime as dt
from django.core.files.base import ContentFile

from celery.result import AsyncResult

#from basic_preprocess import preprocess_csv_file
from ravens_metadata_apps.preprocess_jobs.tasks  import preprocess_csv_file
from ravens_metadata_apps.utils.random_util import get_alphanumeric_lowercase

from ravens_metadata_apps.preprocess_jobs.models import \
    (PreprocessJob, STATE_SUCCESS, STATE_FAILURE)

class JobUtil(object):
    """Convenience class for the preprocess work flow"""

    @staticmethod
    def start_preprocess(job):
        """Start the preprocessing!"""
        assert isinstance(job, PreprocessJob),\
               'job must be a PreprocessJob'

        # job_id = uuid.UUID.time

        # send the file to the queue
        task = preprocess_csv_file.delay(job.source_file.path, job_id=job.id)

        # set the task_id
        job.task_id = task.id

        # update the state of the job
        job.set_state_preprocess_started()

        # save the new state
        job.save()

    @staticmethod
    def check_status(job):
        """Check/update the job status"""
        assert isinstance(job, PreprocessJob),\
               'job must be a PreprocessJob'

        if job.is_finished():
            return

        ye_task = AsyncResult(job.task_id,
                              app=preprocess_csv_file)

        if ye_task.state == 'SUCCESS':

            preprocess_data = ContentFile(json.dumps(ye_task.result['data']))

            new_name = 'preprocess_%s.json' % get_alphanumeric_lowercase(8)
            job.preprocess_file.save(new_name,
                                     preprocess_data)
            job.set_state_success()

            job.user_message = 'Task completed!  Preprocess is available'
            job.end_time = dt.now()
            job.save()
            ye_task.forget()

        elif ye_task.state == 'STATE_FAILURE':
            job.set_state_failure()
            job.user_message = 'ye_task failed....'
            job.save()
            #get_ok_resp('looking good: %s' % (ye_task.result['input_file']),
            #            data=ye_task.result['data']))

            # delete task!

    @staticmethod
    def retrieve_rows(job, **kwargs):

        print('kwargs', kwargs)

        job_id = job.id
        df = pd.read_csv(job.source_file.path)[:100]
        raw_data = df.to_json(orient='split')
        data_back_to_list = json.loads(raw_data)
        print("raw_data", raw_data)

        output = {
            "attributes": {
                    "preprocess_id": job_id,
                    "start_row": 1,
                    "num_rows": 1000,
                    "format": 'json'
                },
                    "data": data_back_to_list,
            }

        #od = json.dumps(output, indent=4)

        return output
