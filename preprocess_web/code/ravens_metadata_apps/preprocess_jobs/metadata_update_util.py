"""Update preprocess metadata, creating a new MetadataUpdate object in the processs"""
import json
from django.core.files.base import ContentFile

from ravens_metadata_apps.utils.random_util import get_alphanumeric_lowercase
from ravens_metadata_apps.preprocess_jobs.job_util import JobUtil
from ravens_metadata_apps.preprocess_jobs.models import MetadataUpdate

class MetadataUpdateUtil(object):

    def __init__(self, preprocess_id, update_json):
        """Initialize with a PreprocessJob id and JSON update snippet"""
        self.preprocess_id = preprocess_id
        self.update_json = update_json

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

    def get_updated_metadata(self):
        """Return the updated metadata"""
        assert self.has_error is False,\
            'Make sure ".has_error" is False before calling this method!'

        return self.metadata_update_obj.get_metadata()


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


        # Make the update!!
        #
        success, update_or_errors = JobUtil.update_preprocess_metadata(\
                                            latest_metadata_or_err,
                                            self.update_json)
        if not success:
            self.add_err_msg(update_or_errors)
            return False

        # ------------------------------------------------------
        # Record successful update in new MetadataUpdate object
        # ------------------------------------------------------
        update_kwargs = dict(update_json=self.update_json)
        if metadata_obj.is_original_metadata():
            # this is a PreprocessJob
            update_kwargs['orig_metadata'] = metadata_obj
            update_kwargs['previous_update'] = None
            update_kwargs['version_number'] = 2
        else:
            # this is a MetadataUpdate object
            update_kwargs['orig_metadata'] = metadata_obj.orig_metadata
            update_kwargs['previous_update'] = metadata_obj
            update_kwargs['version_number'] = metadata_obj.version_number + 1

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
            json_val = json.dumps(update_or_errors)
        except TypeError as err_obj:
            self.add_err_msg('Failed to convert to JSON: %s' % err_obj)
            return False

        new_name = 'update_%s.json' % get_alphanumeric_lowercase(8)
        new_preprocess_data = ContentFile(json_val)

        try:
            self.metadata_update_obj.metadata_file.save(\
                                    new_name,
                                    new_preprocess_data)
        except Exception as err_obj:
            self.add_err_msg('Failed to save metadata update to file: %s' % err_obj)
            return False

        self.metadata_update_obj.save()

        return True