"""Utility class for the preprocess workflow"""
"""Utility class for the preprocess workflow"""
import pandas as pd
from django.http import HttpResponse, JsonResponse

import col_info_constants as col_const
import update_constants as update_const
from preprocess_runner import KEY_JSONLD_CITATION
from ravens_metadata_apps.preprocess_jobs.tasks import \
    (preprocess_csv_file,)
from ravens_metadata_apps.utils.time_util import get_timestring_for_file
from ravens_metadata_apps.utils.basic_response import \
    (ok_resp, err_resp)
from ravens_metadata_apps.preprocess_jobs.models import \
    (PreprocessJob, MetadataUpdate)
from ravens_metadata_apps.metadata_schemas.models import MetadataSchema
from ravens_metadata_apps.metadata_schemas.validation_util import ValidationUtil
from variable_display_util import VariableDisplayUtil
from ravens_metadata_apps.utils.json_util import remove_nan_from_dict
from file_format_constants import TAB_FILE_EXT
from ravens_metadata_apps.utils.view_helper import get_json_error
from custom_statistics_util import CustomStatisticsUtil
from ravens_metadata_apps.utils.view_helper import get_json_error
from ravens_metadata_apps.preprocess_jobs.job_util import JobUtil

class SchemaUtil(object):
    """Convenience class for the metadata schema work flow"""

    # code for metadata schema
    @staticmethod
    def get_latest_schema():
        """to get latest metadata schema"""
        # call to metadata schema

        # Look for the latest update, if it exists
        #
        filters = dict(is_latest=True, is_published=True)
        latest_schema = MetadataSchema.objects.filter(**filters).first()

        # print("here is the data",update_object.name.version_number)
        if not latest_schema:
            return err_resp('Metadata schema not found.')

        schema_ok, schema_or_err = latest_schema.get_schema()
        print('schema status ', schema_ok)
        print('schema', schema_or_err)

        if schema_ok is False:
            return err_resp(schema_or_err)

        return ok_resp(schema_or_err)


    @staticmethod
    def get_schema_version(version):
        """Retrun the version of schema"""

        latest_schema = MetadataSchema.objects.filter(\
                            is_published=True, version=version).first()
        if not latest_schema:
            return err_resp('Metadata schema not found.')

        schema_ok, schema_or_err = latest_schema.get_schema()
        print('schema status ', schema_ok)
        print('schema', schema_or_err)

        if schema_ok is False:
            return err_resp(schema_or_err)

        return ok_resp(schema_or_err)

    @staticmethod
    def validate_preprocess_file(preprocess_id):
        """ Run validator"""

        success, schema_file = SchemaUtil.get_latest_schema()

        if not success:
            return err_resp('schema not found')

        success, data_file = JobUtil.get_latest_metadata(preprocess_id)

        if not success:
            return err_resp(data_file)

        validate = ValidationUtil.run_it(schema_file, data_file)

        if validate:
            return ok_resp(validate)
        else:
            return err_resp(validate)



