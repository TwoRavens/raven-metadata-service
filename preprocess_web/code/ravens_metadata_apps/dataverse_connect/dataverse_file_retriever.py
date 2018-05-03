"""
Retrieve a Dataverse file and create a PreprocessJob object
ref: https://stackoverflow.com/questions/16174022/download-a-remote-image-and-save-it-to-a-django-model
"""
import re
import requests
import tempfile
from os.path import splitext
from django.core import files

from file_format_constants import TAB_FILE_EXT
from ravens_metadata_apps.utils.basic_err_check import BasicErrCheck
from ravens_metadata_apps.preprocess_jobs.models import \
    (PreprocessJob)
from ravens_metadata_apps.utils.random_util import get_alphanumeric_lowercase
from ravens_metadata_apps.utils.url_helper import URLHelper
from ravens_metadata_apps.dataverse_connect.models import \
    (RegisteredDataverse,
     DataverseFileInfo)
import logging

LOGGER = logging.getLogger(__name__)

class DataverseFileRetriever(BasicErrCheck):
    """Download a Dataverse file and save it to a PreprocessJob"""

    def __init__(self, data_file_url, **kwargs):
        """Start with a datafile url
        Options:
        dataverse_citation_url - url to retrive a dataverse JSON-LD citation
        """
        self.data_file_url = data_file_url
        self.dataverse_doi = kwargs.get('dataverse_doi')
        self.dataset_id = kwargs.get('dataset_id')

        self.dv_file_info = None # to hold an instance of DataverseFileInfo

        # to hold an instance of PreprocessJob
        #
        self.preprocess_job = None

        # - Specify a preprocess_job_id to use an existing PreprocessJob
        #     when tracking a celery task id
        #   - BUT: should have no source_file, metadata_file, etc
        #
        self.preprocess_job_id = kwargs.get('preprocess_job_id')

        # default to .tab for Dataverse files
        #
        self.file_extension = kwargs.get('file_ext', TAB_FILE_EXT)

        # optional: retrieve a citation
        #
        self.dataverse_citation_url = kwargs.get('dataverse_citation_url')

        self.run_process()


    def run_process(self):
        """Do your thing...."""
        # do this to have a record of the attempt...
        self.update_preprocess_job()
        self.load_dataverse_info()
        self.run_file_retrieval()

    def update_preprocess_job(self):
        """Update or create the Preprocess Job"""
        if self.preprocess_job_id:
            # There's an existing PreprocessJob to use, let's get it
            try:
                self.preprocess_job = PreprocessJob.objects.get(pk=self.preprocess_job_id)
            except PreprocessJob.DoesNotExist:
                self.preprocess_job = PreprocessJob(name=self.data_file_url)
                err_msg = ('Unable to locate PreprocessJob with id: %d' % \
                           self.preprocess_job_id)
                self.preprocess_job.add_err_msg(err_msg)
                return
        else:
            # Create a new PreprocessJob for this request
            #
            self.preprocess_job = PreprocessJob(name=self.data_file_url)

        self.preprocess_job.set_state_retrieving_data()
        self.preprocess_job.save()


    def add_err_msg(self, err_msg):
        """Add an error message"""
        self.error_found = True
        self.error_message = err_msg

        # Also update the preprocess job
        #
        self.preprocess_job.set_state_failure()
        self.preprocess_job.user_message = err_msg
        self.preprocess_job.save()

    def load_dataverse_info(self):
        """Check if the Dataverse if Registered and if a file id exists"""
        if self.has_error():
            return

        # Get the Datafile id from the url
        #
        dv_id_info = URLHelper.get_datafile_id_from_url(self.data_file_url)
        if not dv_id_info.success:
            self.add_err_msg(dv_id_info.err_msg)
            return

        # Get the network location from the url
        #
        netloc = URLHelper.get_netloc_from_url(self.data_file_url)
        if not netloc.success:
            self.add_err_msg(netloc.err_msg)
            return

        # Retrieve the RegisteredDataverse based on the url network location
        #
        try:
            registered_dv = RegisteredDataverse.objects.get(\
                                    network_location=netloc.result_obj)
        except RegisteredDataverse.DoesNotExist:
            self.add_err_msg("This Dataverse is not registerd: %s" % dv_info.result_obj)
            return

        # Format the url
        #
        #url_to_save = URLHelper.format_datafile_request_url(self.data_file_url)
        #if not url_to_save.success:
        #    self.add_err_msg('Failed to format the url: %s' % url_to_save.err_msg)

        # Start the DataverseFileInfo object--but don't save it yet
        #
        self.dv_file_info = DataverseFileInfo(\
                                    dataverse=registered_dv,
                                    datafile_id=dv_id_info.result_obj)
        if self.dataset_id:
            self.dv_file_info.dataset_id = self.dataset_id
        if self.dataverse_doi:
            self.dv_file_info.dataverse_doi = self.dataverse_doi


    def run_file_retrieval(self):
        """Retrieval the file and save it to a PreprocessJob"""
        if self.has_error():
            return

        # (1) Retrieve the file stream
        #
        LOGGER.debug('(1) Retrieve the file stream')
        file_access_url = self.dv_file_info.get_file_access_url()
        print('file_access_url: ', file_access_url)
        try:
            request = requests.get(file_access_url, stream=True)
        except requests.exceptions.ConnectionError as err_obj:
            user_msg = ('Failed to retrieve file from %s'
                        '\nError: %s') % (self.data_file_url, err_obj)
            self.add_err_msg(user_msg)
            return

        # (2) was the request OK?
        #
        LOGGER.debug('(2) was the request OK?')
        if request.status_code != requests.codes.ok:
            user_msg = ('Failed to retrieve file from %s') % \
                       (self.data_file_url)

            if request.status_code == requests.codes.not_found:
                user_msg = ('%s\nThe file was not found.') % user_msg
            elif request.status_code == requests.codes.forbidden:
                user_msg = ('%s\nThe url is forbidden--likely an unpublished'
                            ' file.') % \
                            user_msg

            user_msg = ('%s\nStatus code: %s') % (user_msg, request.status_code)

            self.add_err_msg(user_msg)
            return

        # (3) Check for the filename and extension
        #
        # example val: "attachment; filename*=UTF-8''FerryDataDepositFinal.mat"
        content_disp = request.headers['content-disposition']
        print('content_disp', content_disp)
        found_list = re.findall(r"filename\*=UTF\-8''(.+)", content_disp)
        if found_list:
            file_name = found_list[0]
            fname_base, fname_ext = splitext(file_name)
            if fname_ext:
                self.file_extension = fname_ext

        output_file_name = 'data_%s_%s%s' % \
                        (self.preprocess_job.id,
                         get_alphanumeric_lowercase(8),
                         self.file_extension)

        # (3a) Read stream to a temporary file
        #
        LOGGER.debug('(3) Read stream to a temporary file')
        named_temp_file = tempfile.NamedTemporaryFile()

        # Read the streamed image in sections
        #
        for block in request.iter_content(1024 * 8):
            # If blocks, then stop
            if not block:
                break
            # Write image block to temporary file
            named_temp_file.write(block)

        # (4) Link the file to a new PreprocessJob
        #
        LOGGER.debug('(4) Link the file to a new PreprocessJob')
        #

        self.preprocess_job.source_file.save(\
                        output_file_name,
                        files.File(named_temp_file))

        self.preprocess_job.set_state_data_retrieved()
        self.preprocess_job.save()

        # Update and save the instance of DataverseFileInfo
        #
        self.dv_file_info.preprocess_job = self.preprocess_job
        self.dv_file_info.save()
