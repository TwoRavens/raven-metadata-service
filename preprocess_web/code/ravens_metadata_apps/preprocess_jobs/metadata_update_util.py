"""Update preprocess metadata, creating a new MetadataUpdate object in the processs"""
import json

from decimal import Decimal

from django.core.files.base import ContentFile
from ravens_metadata_apps.utils.random_util import get_alphanumeric_lowercase
from ravens_metadata_apps.preprocess_jobs.job_util import JobUtil

from ravens_metadata_apps.preprocess_jobs.models import MetadataUpdate
from custom_statistics_util import CustomStatisticsUtil

from variable_display_util import VariableDisplayUtil
from np_json_encoder import NumpyJSONEncoder
from col_info_constants import \
    (UPDATE_VARIABLE_DISPLAY, UPDATE_CUSTOM_STATISTICS,DELETE_CUSTOM_STATISTICS,UPDATE_TO_CUSTOM_STATISTICS)


class MetadataUpdateUtil(object):

    def __init__(self, preprocess_id, update_json, update_type=None):
        """Initialize with a PreprocessJob id and JSON update snippet"""
        if not update_type:
            update_type = UPDATE_VARIABLE_DISPLAY

        self.preprocess_id = preprocess_id
        self.update_json = update_json
        self.update_type = update_type

        # to be created...
        self.metadata_update_obj = None

        # to track internal errs
        self.has_error = False
        self.error_messages = []

        self.make_update()

    def add_err_msg(self, err_msg):
        """Create an error message and flip the 'has_error' flag"""
        self.has_error = True

        if isinstance(err_msg, list):
            # In case a list is returned from the update processs
            self.error_messages = err_msg
        else:
            self.error_messages.append(err_msg)

    def get_error_messages(self):
        """Return the list of error messages"""
        print("Error messages ", self.error_messages)
        return self.error_messages

    def get_updated_metadata(self, as_obj=False):
        """Return the updated metadata dict or obj"""
        assert self.has_error is False,\
            'Make sure ".has_error" is False before calling this method!'

        success, metadata = self.metadata_update_obj.get_metadata()
        assert success is True, \
            "MetadataUpdate object with id %s should have valid metadata" % \
            self.metadata_update_obj.id

        if as_obj:
            return self.metadata_update_obj

        return metadata

    def get_update_util(self, latest_metadata_or_err):
        """Either update the variable display or the summary stats"""

        if self.update_type == UPDATE_VARIABLE_DISPLAY:

            return VariableDisplayUtil(latest_metadata_or_err, self.update_json)

        elif self.update_type == UPDATE_CUSTOM_STATISTICS:
            var_util = CustomStatisticsUtil(latest_metadata_or_err, self.update_json)
            var_util.custom_statistics_update()
            return var_util

        elif self.update_type == UPDATE_TO_CUSTOM_STATISTICS:
            update_util = CustomStatisticsUtil(latest_metadata_or_err, self.update_json)
            update_util.update_custom_stats()
            return update_util

        elif self.update_type == DELETE_CUSTOM_STATISTICS:
            delete_util = CustomStatisticsUtil(latest_metadata_or_err, self.update_json)
            delete_util.delete_custom_stat()
            return delete_util

        else:
            self.add_err_msg('Unknown update type: %s' % self.update_type)
            return None

    def make_update(self):
        """Update the latest version of the preprocess metadata"""

        # Retrieve either a PreprocessJob or MetadataUpdate
        #
        success, metadata_obj_or_err = JobUtil.get_latest_metadata_object(self.preprocess_id)

        if not success:
            self.add_err_msg(metadata_obj_or_err)
            return False
        else:
            metadata_obj = metadata_obj_or_err  # to be clear

        # Retrieve the metadata from a file; returned as an OrderedDict
        #
        data_found, latest_metadata_or_err = metadata_obj_or_err.get_metadata()

        if not data_found:
            self.add_err_msg(latest_metadata_or_err)
            return False

        #  Make the update!!
        #
        # success, update_or_errors = JobUtil.update_preprocess_metadata(\
        #                                    latest_metadata_or_err,
        #                                    self.update_json)

        # var_util = VariableDisplayUtil(latest_metadata_or_err, self.update_json)

        var_util = self.get_update_util(latest_metadata_or_err)

        if var_util is None:
            self.add_err_msg(var_util.get_error_messages())
            return False
        elif var_util.has_error:
            self.add_err_msg(var_util.get_error_messages())
            return False

        # ------------------------------------------------------
        # Record successful update in new MetadataUpdate object
        # ------------------------------------------------------
        update_kwargs = dict(update_json=self.update_json)
        if metadata_obj.is_original_metadata():  # Is this a PreprocssJob
            # this is a PreprocessJob
            update_kwargs['orig_metadata'] = metadata_obj
            update_kwargs['previous_update'] = None
            if var_util.is_major_update():
                update_kwargs['version_number'] = Decimal('2')
            else:
                update_kwargs['version_number'] = Decimal('1.1')
        else:
            # this is a MetadataUpdate object
            update_kwargs['orig_metadata'] = metadata_obj.orig_metadata
            update_kwargs['previous_update'] = metadata_obj
            if var_util.is_major_update():
                new_num = Decimal(int(metadata_obj.version_number + Decimal('1')))
                update_kwargs['version_number'] = new_num
            else:
                update_kwargs['version_number'] = metadata_obj.version_number + Decimal('.1')

        # ------------------------------------------------------
        # Create the object....
        # ------------------------------------------------------
        self.metadata_update_obj = MetadataUpdate(**update_kwargs)
        self.metadata_update_obj.save()

        # ------------------------------------------------------
        # Write the updated metadata to a file
        #  + attach it to the MetadataUpdate
        # ------------------------------------------------------
        try:
            json_val = json.dumps(var_util.get_updated_metadata(),
                                  cls=NumpyJSONEncoder)
        except TypeError as err_obj:
            # delete the MetadataUpdate
            self.metadata_update_obj.delete()
            self.add_err_msg(
                ('Failed to convert to JSON: %s'
                 ' (MetadataUpdateUtil: 118)') % err_obj)
            return False

        new_name = 'update_%s_%s.json' % (self.metadata_update_obj.id, get_alphanumeric_lowercase(8))
        json_val = json_val.encode('utf-8')
        new_preprocess_data = ContentFile(json_val)

        try:
            self.metadata_update_obj.metadata_file.save(
                                    new_name,
                                    new_preprocess_data)
        except Exception as err_obj:
            self.add_err_msg('Failed to save metadata update to file: %s' % err_obj)
            return False

        self.metadata_update_obj.save()

        return True
