"""Convenience methods for processing Dataverse files"""
from ravens_metadata_apps.preprocess_jobs.models import PreprocessJob
from ravens_metadata_apps.dataverse_connect.models import DataverseFileInfo
from ravens_metadata_apps.dataverse_connect.tasks import preprocess_dataverse_file
from ravens_metadata_apps.utils.url_helper import URLHelper
from ravens_metadata_apps.utils.basic_response import \
    (ok_resp, err_resp)

class DataverseUtil(object):
    """Methods related to Dataverse files"""


    @staticmethod
    def get_existing_dataverse_file_info(data_file_url):
        """Examine the url and see if we already have metadata for this file"""
        # Get the Datafile id from the url
        #
        dv_id_info = URLHelper.get_datafile_id_from_url(data_file_url)
        if not dv_id_info.success:
            return err_resp(dv_id_info.err_msg)

        # Get the network location from the url
        #
        netloc = URLHelper.get_netloc_from_url(data_file_url)
        if not netloc.success:
            return err_resp(netloc.err_msg)


        try:
            dv_file_info = DataverseFileInfo.objects.get(\
                            dataverse__network_location=netloc.result_obj,
                            datafile_id=dv_id_info.result_obj)
        except DataverseFileInfo.DoesNotExist:
            return err_resp('DataverseFileInfo not found.')

        return ok_resp(dv_file_info)


    @staticmethod
    def process_dataverse_file(data_file_url, dataset_id=None):
        """Create a PreprocessJob, download a DataverseFile and preprocess it!"""
        assert data_file_url, "data_file_url must be specified"

        # Check for an existing PreprocessJob related to this file
        #
        existing_info = DataverseUtil.get_existing_dataverse_file_info(data_file_url)
        if existing_info.success:
            print('It already exists!!!')
            return ok_resp(existing_info.result_obj.preprocess_job)

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

        return ok_resp(job)
