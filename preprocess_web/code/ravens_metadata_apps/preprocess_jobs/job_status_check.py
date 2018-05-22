"""Utility class for the preprocess workflow"""
import json
from django.core.files.base import ContentFile
from django.utils import timezone
from celery.result import AsyncResult
from ravens_metadata_apps.preprocess_jobs.tasks  import preprocess_csv_file
from ravens_metadata_apps.utils.random_util import get_alphanumeric_lowercase
from ravens_metadata_apps.utils.basic_response import \
    (ok_resp, err_resp)
from ravens_metadata_apps.preprocess_jobs.models import \
    (PreprocessJob,
     STATE_SUCCESS, STATE_FAILURE)


class JobStatusCheck(object):
    """Check celery and update status for a PreprocessJob"""

    @staticmethod
    def check_status_by_job_id(job_id):
        """Check/update the job status by job_id"""
        print('=' * 40)
        print('check_status_by_job_id', job_id)
        print('=' * 40)

        try:
            job = PreprocessJob.objects.get(job_id)
        except PreprocessJob.DoesNotExist:
            user_msg = ('PreprocessJob not found: %s'
                        ' (check_status_by_job_id)') % (job_id)
            return err_resp(user_msg)

        it_worked = JobStatusCheck.check_status(job)
        if it_worked:
            return ok_resp(job)

        user_msg = ('PreprocessJob still in process: %s') % (job_id)
        return err_resp(user_msg)


    @staticmethod
    def xcheck_status(job):
        """Check/update the job status"""
        assert isinstance(job, PreprocessJob),\
               'job must be a PreprocessJob'

        if job.is_finished():
            return True

        ye_task = AsyncResult(job.task_id,
                              app=preprocess_csv_file)

        if ye_task.state == 'SUCCESS':

            if ye_task.result['success']:

                preprocess_data = ContentFile(json.dumps(ye_task.result['data']))

                new_name = 'preprocess_%s_%s_%s.json' % \
                           (job.id,
                            job.get_version_string(as_slug=True),
                            get_alphanumeric_lowercase(8))

                job.metadata_file.save(new_name,
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
