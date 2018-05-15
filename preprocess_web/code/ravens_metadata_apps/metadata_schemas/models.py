from django.db import models
from django.urls import reverse
from django.conf import settings
# For the prototype, set the current schema for now...

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
