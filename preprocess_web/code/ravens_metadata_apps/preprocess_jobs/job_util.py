"""Utility class for the preprocess workflow"""
from ravens_metadata_apps.preprocess_jobs.models import \
    (PreprocessJob, STATE_SUCCESS, STATE_FAILURE)

from celery.result import AsyncResult

from basic_preprocess import preprocess_csv_file
from random_util import get_alphanumeric_lowercase


class JobUtil(object):
    """Convenience class for the preprocess work flow"""

    @staticmethod
    def start_preprocess(job):
        """Start the preprocessing!"""
        assert isinstance(job, PreprocessJob),\
               'job must be a PreprocessJob'

        # send the file to the queue
        task = preprocess_csv_file.delay(job.source_file.path)

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
            job.set_state_success()
            job.user_message = ye_task.result['data']
            job.save()
            ye_task.forget()
        elif ye_task.state == 'STATE_FAILURE':
            job.set_state_failure()
            job.user_message = 'ye_task failed....'
            job.save()
            #get_ok_resp('looking good: %s' % (ye_task.result['input_file']),
            #            data=ye_task.result['data']))

            # delete task!
