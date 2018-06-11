from django.db import models
from django.urls import reverse
from django.conf import settings
# For the prototype, set the current schema for now...
from model_utils.models import TimeStampedModel

PREPROCESS_CORE_METADATA = 'PREPROCESS_CORE_METADATA'


class MetadataSchema(TimeStampedModel):
    """ model for metadata schema"""
    name = models.CharField(blank=False,
                            max_length=255,
                            unique=True)

    schema_type = models.CharField(default=PREPROCESS_CORE_METADATA,
                                   max_length=255)
    version = models.CharField(max_length=50,
                               unique=True)
    is_published = models.BooleanField(default=False)
    is_latest = models.BooleanField(default=True)
    schema_file = models.FileField(upload_to='schema_files/%Y/%m/%d/',
                                   blank=False)
    description = models.TextField(blank=True)


def get_temp_schema_info():
    # ------------------------------------------
    # some premodel variables for the prototype
    # ------------------------------------------
    SCHEMA_TEMP_NAME = 'TwoRavens Metadata File Schema'
    SCHEMA_TEMP_VERSION = 'v0.4-alpha'
    SCHEMA_TEMP_LINK = '%s://%s%s' % \
                       (settings.SITE_SCHEME,
                        settings.SWAGGER_HOST,
                        reverse('view_latest_metadata_schema', args=()))
    SCHEMA_TEMP_DOCS_LINK = ('http://two-ravens-metadata-service.readthedocs.io/'
                             'en/latest/preprocess_file_description.html'
                             '#preprocess-parameters')
    # ------------------------------------------

    SCHEMA_INFO_DICT = dict(name=SCHEMA_TEMP_NAME,
                            version=SCHEMA_TEMP_VERSION,
                            schema_url=SCHEMA_TEMP_LINK,
                            schema_docs=SCHEMA_TEMP_DOCS_LINK)
    return SCHEMA_INFO_DICT

