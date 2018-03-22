"""Utility class for the preprocess workflow"""
import json, uuid
import pandas as pd
from collections import OrderedDict
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
        start_row = kwargs.get('start_row')
        num_rows = kwargs.get('number_rows')
        format_value = kwargs.get('format')
        update_end_num = start_row + num_rows
        # we can check for max_rows and other conditions using the metadata information ( to be implemented later)
        # if start_row <= 0 or num_rows <= 0 or format_value is None or job is None:
        #     user_msg = dict(success=False,
        #                     message='The input is incorrect',
        #                     input=kwargs)
        #
        #     return user_msg
        # else:
        job_id = job.id

        csv_data = pd.read_csv(job.source_file.path)
        max_rows = len(csv_data)
        print("the no. of rows are ", max_rows)

        error_message = []

        if start_row > max_rows:
            err = 'The request was from %s rows but only %d rows were found, so default start rows = 1 is set' % (start_row, max_rows)
            error_message.append(err)
            start_row = 1
        elif num_rows > max_rows:
            err = 'The request was for %s rows but only %d rows were found, so number rows is set to max rows' % (num_rows, max_rows)
            error_message.append(err)
            num_rows = max_rows

        print("error message", error_message)
        data_frame = csv_data[start_row:update_end_num]

        # if the format is json
        if format_value is 'json':
            raw_data = data_frame.to_dict(orient='split')

            print("raw_data", raw_data)

            if len(error_message) > 0:
                output = {
                    "success": True,
                    "message": 'It worked but with some changes',
                    "modifications": error_message,
                    "attributes": {
                        "preprocess_id": job_id,
                        "start_row": start_row,
                        "num_rows": num_rows,
                        "format": format_value
                    },
                    "data": str(raw_data),
                }

            else:
                output = {
                    "success": True,
                    "message": 'It worked',
                    "attributes": {
                        "preprocess_id": job_id,
                        "start_row": start_row,
                        "num_rows": num_rows,
                        "format": format_value
                    },
                    "data": str(raw_data),
                }

            return output

        # if the format is csv
        else:
            return
