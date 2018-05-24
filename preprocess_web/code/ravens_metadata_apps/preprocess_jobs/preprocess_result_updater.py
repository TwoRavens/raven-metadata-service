"""Hold the results of a celery preprocess run and update
the PreprocessJob appropriately"""
import json
from django.utils import timezone
from ravens_metadata_apps.preprocess_jobs.models import \
    (PreprocessJob,
     STATE_SUCCESS, STATE_FAILURE)
from ravens_metadata_apps.utils.random_util import get_alphanumeric_lowercase
from ravens_metadata_apps.utils.json_util import json_dump
from django.core.files.base import ContentFile


class PreprocessResultUpdater(object):
    """Convenience class for updating preprocess"""
    def __init__(self, success=False, job_id=None, user_message=None, **kwargs):
        self.success = success
        self.job_id = job_id
        self.user_message = user_message
        self.input_file = kwargs.get('input_file', None)
        self.preprocess_data = kwargs.get('data', None)
        self.elapsed_time = kwargs.get('elapsed_time', None)

        # ----------
        self.has_error = False
        self.error_message = None

        self.update_preprocess_job()

    def add_error_message(self, err_msg):
        """Add error message"""
        self.has_error = True
        self.error_message = err_msg

    def update_preprocess_job(self):
        """Retrieve the PreprocessJob and update it"""
        try:
            job = PreprocessJob.objects.get(pk=self.job_id)
        except PreprocessJob.DoesNotExist:
            user_msg = ('PreprocessJob not found: %s'
                        ' (check_status_by_job_id)') % (self.job_id)
            self.add_error_message(user_msg)
            return

        # Preprocess failed!
        #
        if self.success is not True:
            job.set_state_failure(self.user_message)
            job.save()
            return

        # Preprocess worked!
        #
        dump_result = json_dump(self.preprocess_data)
        if not dump_result.success:
            job.set_state_failure(dump_result.err_msg)
            job.source_file.delete()
            job.save()
            return

        preprocess_string = dump_result.result_obj
        preprocess_string = preprocess_string.encode('utf-8')
        preprocess_content_file = ContentFile(preprocess_string)


        new_name = 'preprocess_%s_%s_%s.json' % \
                   (job.id,
                    job.get_version_string(as_slug=True),
                    get_alphanumeric_lowercase(8))

        job.metadata_file.save(new_name,
                               preprocess_content_file)
        job.set_state_success()

        job.user_message = 'Task completed!  Preprocess is available'
        job.save()
