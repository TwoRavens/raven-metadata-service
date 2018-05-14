from collections import OrderedDict
from urllib.parse import urlunparse

import jsonfield

from model_utils.models import TimeStampedModel
from django.db import models

from ravens_metadata_apps.preprocess_jobs.models import PreprocessJob
from ravens_metadata_apps.dataverse_connect.dv_constants import PATH_DATAFILE_ACCESS

from ravens_metadata_apps.utils.url_helper import URLHelper


class RegisteredDataverse(TimeStampedModel):
    """
    Dataverses that are allowed to use this service
    """
    name = models.CharField(unique=True, max_length=255)

    dataverse_url = models.URLField(\
                    unique=True,
                    help_text='Example: "https://dataverse.harvard.edu"')

    url_scheme = models.CharField(\
                    max_length=10,
                    blank=True,
                    help_text='Created on save. Used for API formatting')

    network_location = models.CharField(\
                            max_length=255,
                            blank=True,
                            help_text='Created on save. Used for matching')

    active = models.BooleanField(default=True)

    notes = models.TextField(blank=True, help_text='optional')


    class Meta:
        """Set the ordering"""
        ordering = ('name',)

    def __str__(self):
        """str representation"""
        if self.network_location:
            return self.network_location

        return self.name
        #return '%s (%s)' % (self.name, self.network_location)

    def save(self, *args, **kwargs):
        """Standardize the url on save"""
        update_url_info = URLHelper.set_netloc_and_scheme(self.dataverse_url, self)
        assert update_url_info.success, \
            "There is something wrong with the url: %s" % update_url_info.err_msg

        super(RegisteredDataverse, self).save(*args, **kwargs)


    def get_potential_file_url(self):
        """subject to change, append query params to show tabular files"""

        query_params = ('q=&fq0=fileTypeGroupFacet%3A"tabulardata"'
                        '&fq1=fileAccess%3A"Public"'
                        '&types=files&sort=dateSort'
                        '&order=desc')

        return ('{0}://{1}?{2}').format(\
                 self.url_scheme,
                 self.network_location,
                 query_params)

    def get_search_api_url(self, file_id):
        """Construct a url for using the search API for a file"""
        # example:
        # https://dataverse.harvard.edu/api/search?q=entityId:$FILEID

        return ('{0}://{1}/api/search?q=entityId:{2}').format(\
                    self.url_scheme,
                    self.network_location,
                    file_id)

    def get_file_access_url(self, file_id):
        """Build a url similar to:
        https://dataverse.harvard.edu/api/access/datafile/{{ file id }}
        """
        params = (self.url_scheme,
                  self.network_location,
                  '%s%s' % (PATH_DATAFILE_ACCESS, file_id),
                  None, None, None)

        return urlunparse(params)


    def get_jsonld_url(self, doi_str):
        """Construct a url for retrieving the citation in JSON-LD format
        example: https://dataverse.harvard.edu/api/datasets/export?exporter=schema.org&persistentId=doi%3A10.7910/DVN/ROLEY5"""
        doi_str = doi_str.replace('doi', 'doi:').replace('.org/', '')

        return ('{0}://{1}/api/datasets/export?exporter=schema.org&persistentId={2}').format(\
                self.url_scheme,
                self.network_location,
                doi_str)

class DataverseFileInfo(TimeStampedModel):
    """Information about Preprocessed DataverseFile"""
    preprocess_job = models.ForeignKey(PreprocessJob,
                                       on_delete=models.CASCADE)

    dataverse = models.ForeignKey(RegisteredDataverse,
                                  on_delete=models.CASCADE)

    datafile_id = models.IntegerField('Datafile Id')

    #version = models.CharField(max_length=50,
    #                           help_text='Dataverse file version',
    #                           blank=True)
    dataset_id = models.IntegerField('Dataverse dataset Id',
                                     default=-1)

    dataset_doi = models.CharField('DOI',
                                   max_length=255,
                                   blank=True)

    original_filename = models.CharField('original filename',
                                         max_length=255,
                                         blank=True)

    formatted_citation = models.TextField(blank=True)

    jsonld_citation = jsonfield.JSONField(\
                        load_kwargs=dict(object_pairs_hook=OrderedDict))

    def __str__(self):
        """display name"""
        if self.dataset_doi:
            return '{0} ({1})'.format(self.datafile_id, self.dataset_doi)

        return '{0}'.format(self.datafile_id)


    class Meta:
        unique_together = ('dataverse',
                           'datafile_id',
                           'preprocess_job')
        verbose_name = 'Dataverse File Information'
        verbose_name_plural = 'Dataverse File Information'

    def get_file_access_url(self):
        """Build a url similar to:
        https://dataverse.harvard.edu/api/access/datafile/{{ file id }}
        """
        if not self.dataverse:
            return None

        return self.dataverse.get_file_access_url(self.datafile_id)
