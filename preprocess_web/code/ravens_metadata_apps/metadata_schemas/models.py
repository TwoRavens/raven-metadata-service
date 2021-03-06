import json
import decimal
from django.db import models
from django.urls import reverse
from django.conf import settings
from django.utils.text import slugify
from django.db import transaction

import jsonfield
from collections import OrderedDict
# For the prototype, set the current schema for now...
from model_utils.models import TimeStampedModel
from ravens_metadata_apps.raven_auth.models import User
from ravens_metadata_apps.utils.json_util import json_dump
from ravens_metadata_apps.utils.basic_response import \
    (ok_resp, err_resp)
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
    is_published = models.BooleanField(default=True)
    is_latest = models.BooleanField(default=True)

    schema_json = jsonfield.JSONField(\
                    load_kwargs=dict(object_pairs_hook=OrderedDict))


    #schema_file = models.FileField(upload_to='schema_files/%Y/%m/%d/',
    #                               null=True
    #                               blank=True)

    description = models.TextField(blank=True)

    class Meta:
        ordering = ('-id',)

    @transaction.atomic
    def save(self, *args, **kwargs):
        """make sure there is only one 'is_latest' """
        if not self.id:
            super(MetadataSchema, self).save(*args, **kwargs)

        # If this is the default, set everything else to non-default
        if self.is_latest:
            MetadataSchema.objects.filter(is_latest=True\
                            ).exclude(id=self.id\
                            ).update(is_latest=False)

        super(MetadataSchema, self).save(*args, **kwargs)

    def get_schema(self, as_string=False):
        """Return preprocess file contents if they exist"""
        if as_string:
            return json_dump(self.schema_json, indent=4)

        return ok_resp(self.schema_json)

        """
        if not self.schema_file:
            return err_resp('No schema data. e.g. No file')

        try:
            self.schema_file.open(mode='r')
            file_data = self.schema_file.read()
            self.schema_file.close()
        except FileNotFoundError:
            return err_resp('schema file not found for job id: %s' % self.id)

        if isinstance(file_data, bytes):
            file_data = file_data.decode('utf-8')

        try:
            json_dict = json.loads(file_data,
                                   object_pairs_hook=OrderedDict,
                                   parse_float=decimal.Decimal)
        except ValueError:
            return err_resp('File contained invalid JSON! (%s)' % \
                            (self.schema_file))

        if as_string:
            return json_dump(json_dict, indent=4)

        return ok_resp(json_dict)
        """

    def get_schema_as_json(self):
        """For display, return preprocess file as string if it exists"""
        success, info = self.get_schema(as_string=True)

        return info

    def get_version_string(self, as_slug=False):
        """Return the version in string format"""
        # print("string version_number", str(self.version_number))
        # 3.0 => '3.0'
        if as_slug:
            return slugify(str(self.version))

        return str(self.version)




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
