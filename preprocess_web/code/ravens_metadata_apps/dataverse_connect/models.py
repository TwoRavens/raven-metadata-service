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
        return '%s (%s)' % (self.name, self.dataverse_url)

    def save(self, *args, **kwargs):
        """Standardize the url on save"""
        update_url_info = URLHelper.set_netloc_and_scheme(self.dataverse_url, self)
        assert update_url_info.success, \
            "There is something wrong with the url: %s" % update_url_info.err_msg

        super(RegisteredDataverse, self).save(*args, **kwargs)



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

    dataverse_doi = models.CharField('DOI',
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
        if self.dataverse_doi:
            return '{0} ({1})'.format(self.datafile_id, self.dataverse_doi)

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
        params = (self.dataverse.url_scheme,
                  self.dataverse.network_location,
                  '%s%s' % (PATH_DATAFILE_ACCESS, self.datafile_id),
                  None, None, None)

        print('params: ', params)
        return urlunparse(params)
