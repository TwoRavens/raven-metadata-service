from collections import OrderedDict

import jsonfield
from model_utils.models import TimeStampedModel

from django.db import models

from ravens_metadata_apps.preprocess_jobs.models import PreprocessJob
from ravens_metadata_apps.utils.url_helper import URLHelper


class RegisteredDataverse(TimeStampedModel):
    """
    Dataverses that are allowed to use this service
    """
    name = models.CharField(unique=True, max_length=255)

    dataverse_url = models.URLField(\
                    unique=True,
                    help_text='Example: "https://dataverse.harvard.edu"')

    network_location = models.CharField(\
                            max_length=255,
                            blank=True,
                            help_text='Created on save. Used for matching')

    active = models.BooleanField(default=True)

    notes = models.TextField(blank=True, help_text='optional')


    class Meta:
        ordering = ('name',)

    def __str__(self):
        return '%s (%s)' % (self.name, self.dataverse_url)

    def save(self, *args, **kwargs):
        """Standardize the url on save"""
        while self.dataverse_url and self.dataverse_url.endswith('/'):
            self.dataverse_url = self.dataverse_url[:-1]

        self.dataverse_url = self.dataverse_url.lower()

        self.network_location = urlparse(self.dataverse_url).netloc

        super(RegisteredDataverse, self).save(*args, **kwargs)



class DataverseFile(TimeStampedModel):
    """Information about Preprocessed DataverseFile"""
    preprocess_job = models.ForeignKey(PreprocessJob,
                                       on_delete=models.CASCADE)

    dataverse = models.ForeignKey(RegisteredDataverse,
                                  on_delete=models.CASCADE)

    datafile_id = models.IntegerField('Datafile Id')

    dataverse_doi = models.CharField('DOI',
                                     max_length=255,
                                     blank=True)

    formatted_citation = models.TextField(blank=True)

    jsonld_citation = jsonfield.JSONField(\
                        load_kwargs=dict(object_pairs_hook=OrderedDict))

    def __str__(self):
        """display name"""
        if self.doi:
            return '{0} ({1})'.format(self.datafile_id, self.doi)

        return '{0}'.format(self.doi)

    class Meta:
        unique_together = ('dataverse',
                           'datafile_id',
                           'preprocess_job')
