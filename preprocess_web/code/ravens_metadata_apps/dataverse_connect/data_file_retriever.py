"""
Retrieve a Dataverse file and create a PreprocessJob object
ref: https://stackoverflow.com/questions/16174022/download-a-remote-image-and-save-it-to-a-django-model
"""
import requests
import tempfile

from django.core import files

from file_format_constants import TAB_FILE_EXT
from ravens_metadata_apps.utils.basic_err_check import BasicErrCheck
from ravens_metadata_apps.preprocess_jobs.models import \
    (PreprocessJob)
from ravens_metadata_apps.utils.random_util import get_alphanumeric_lowercase
import logging

LOGGER = logging.getLogger(__name__)

class DataFileRetriever(BasicErrCheck):
    """Download a Dataverse file and save it to a PreprocessJob"""

    def __init__(self, data_file_url, **kwargs):
        """Start with a datafile url
        Options:
        dataverse_citation_url - url to retrive a dataverse JSON-LD citation
        """
        self.data_file_url = data_file_url
        self.preprocess_job = None  # to hold an instance of PreprocessJob

        # default to .tab for Dataverse files
        #
        self.file_extension = kwargs.get('file_ext', TAB_FILE_EXT)

        # optional: retrieve a citation
        #
        self.dataverse_citation_url = kwargs.get('dataverse_citation_url')

        self.run_process()

    def run_process(self):
        """Do your thing...."""

        # (1) Retrieve the file stream
        #
        LOGGER.debug('(1) Retrieve the file stream')
        try:
            request = requests.get(self.data_file_url, stream=True)
        except requests.exceptions.ConnectionError as err_obj:
            user_msg = ('Failed to retrieve file from %s'
                        '\nError: %s') % (self.data_file_url, err_obj)
            self.add_err_msg(user_msg)
            return

        # (2) was the request OK?
        #
        LOGGER.debug('(2) was the request OK?')
        if request.status_code != requests.codes.ok:
            user_msg = ('Failed to retrieve file from %s'
                        '\nStatus code: %s') % \
                        (self.data_file_url, request.status_code)
            self.add_err_msg(user_msg)
            return

        # (3) Read stream to a temporary file
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
        self.preprocess_job = PreprocessJob(name=self.data_file_url)
        self.preprocess_job.save() # save it to get the id

        # Get the filename from the url, used for saving later
        file_name = 'data_%s_%s%s' % \
                    (self.preprocess_job.id,
                     get_alphanumeric_lowercase(8),
                     self.file_extension)

        self.preprocess_job.source_file.save(\
                        file_name,
                        files.File(named_temp_file))
