"""Convenience methods for processing Dataverse files"""
from ravens_metadata_apps.preprocess_jobs.models import PreprocessJob
from ravens_metadata_apps.dataverse_connect.tasks import preprocess_dataverse_file

class DataverseUtil(object):
    """Methods related to Dataverse files"""

    @staticmethod
    def process_dataverse_file(data_file_url, dataset_id=None):
        """Create a PreprocessJob, download a DataverseFile and preprocess it!"""
        assert data_file_url, "data_file_url must be specified"

        # create a PreprocessJob with only a name and state
        #
        job = PreprocessJob(name=data_file_url)
        job.set_state_pending()
        job.save()

        # Start the download/preprocess
        #
        task = preprocess_dataverse_file.delay(\
                        data_file_url,
                        preprocess_job_id=job.id,
                        dataset_id=dataset_id)

        # save the celery task_id as a reference
        #
        job.task_id = task.id
        job.save()

        return job
