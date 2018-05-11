"""
Running individual tests

python manage.py test ravens_metadata_apps.preprocess_jobs.tests.test_file_encoding
"""
from os.path import abspath, dirname, isdir, isfile, join
import json
from decimal import Decimal
from unittest import skip

from django.test import TestCase
from django.core.files.base import ContentFile
from django.template.loader import render_to_string

from msg_util import msgt

import col_info_constants as col_const
import update_constants as update_const

from ravens_metadata_apps.preprocess_jobs.models import PreprocessJob
from ravens_metadata_apps.utils.random_util import get_alphanumeric_lowercase
from ravens_metadata_apps.utils.time_util import get_timestring_for_file
from ravens_metadata_apps.preprocess_jobs.models import MetadataUpdate
from ravens_metadata_apps.preprocess_jobs.metadata_update_util import \
    (MetadataUpdateUtil)

TEST_FILE_DIR = join(dirname(abspath(__file__)), 'test_files')


class FileEncodingTestCase(TestCase):

    def setUp(self):
        """Set up PreprocessJobs"""
        self.code_book_description = "code book label"

        self.job_01_text = self.get_preprocess_job_with_file()

        self.job_02_binary = self.get_preprocess_job_with_file(as_binary=True)

    def tearDown(self):
        """Set up PreprocessJobs"""
        print('    - remove test files')
        self.job_01_text.metadata_file.delete()
        self.job_02_binary.metadata_file.delete()

    def delete_metadata_files(self, preprocess_id):
        """Delete metadata files"""
        for metadata_obj in MetadataUpdate.objects.filter(orig_metadata=preprocess_id):
            # delete the associated metadata file...
            if metadata_obj.metadata_file:
                metadata_obj.metadata_file.delete()

    def get_metadata_obj(self, job_obj, **kwargs):
        """Create a new Metadata object using a PreprocessJob"""
        viewable = kwargs.get('viewable', True)
        omit_list = kwargs.get('omit_list', ['mean', 'median'])
        description = kwargs.get(col_const.DESCRIPTION_LABEL, 'code book label')

        update_str = """{
                       "%s": %s,
                       "%s":{
                          "ccode":{
                             "viewable":true,
                             "omit":[
                                "mean",
                                "median"
                             ],
                             "%s":{
                                "%s": "%s"
                             }
                          }
                       }
                    }""" % \
                     (col_const.PREPROCESS_ID,
                      job_obj.id,
                      update_const.VARIABLE_UPDATES,
                      update_const.VALUE_UPDATES_KEY,
                      col_const.DESCRIPTION_LABEL,
                      self.code_book_description)

        #   print('update_str', update_str)

        update_json = json.loads(update_str)

        # viewable for minor update
        update_json[update_const.VARIABLE_UPDATES]['ccode']['viewable'] = viewable
        update_json[update_const.VARIABLE_UPDATES]['ccode']['omit'] = omit_list
        update_json[update_const.VARIABLE_UPDATES]['ccode'][update_const.VALUE_UPDATES_KEY]\
                                                           [col_const.DESCRIPTION_LABEL] = description

        update_util = MetadataUpdateUtil(job_obj.id, update_json)

        assert update_util.has_error is False,\
            "There shouldn't be an error!"

        return update_util.get_updated_metadata(as_obj=True)

    def get_preprocess_job_with_file(self, as_binary=False):
        """Create a new PreprocessJob with a preprocess_file"""
        kwargs = dict(name='job 01')
        ye_job = PreprocessJob(**kwargs)
        ye_job.save()

        preprocess_string = render_to_string(
                                'preprocess/test_files/fearon_laitin.json',
                                dict(preprocess_id=ye_job.id))

        if as_binary:
            preprocess_string = preprocess_string.encode()

        preprocess_content_file = ContentFile(preprocess_string)

        new_name = 'preprocess_%s_%s_%s_%s.json' % \
                   (ye_job.id,
                    ye_job.get_version_string(as_slug=True),
                    get_timestring_for_file(),
                    get_alphanumeric_lowercase(8))

        ye_job.metadata_file.save(new_name,
                                  preprocess_content_file)

        #   print('    - create test file:', ye_job.metadata_file.path)

        ye_job.set_state_success()
        ye_job.save()

        return ye_job

    #   @skip('skipit')
    def test_10_get_metadata(self):
        """Read metadata that has a text file encoding"""
        msgt(self.test_10_get_metadata.__doc__)

        # Open text file, return dict
        #
        metadata = self.job_01_text.get_metadata()

        #   print('type(metadata.result_obj)', type(metadata.result_obj))
        self.assertTrue(metadata.success)

        self.assertEqual(\
            metadata.result_obj[col_const.DATASET_LEVEL_KEY][col_const.DATASET_ROW_CNT],
            6610)

        self.assertEqual(\
            metadata.result_obj[col_const.DATASET_LEVEL_KEY][col_const.DATASET_ROW_CNT],
            6610)

        self.assertEqual(\
            metadata.result_obj[col_const.SELF_SECTION_KEY][col_const.VERSION_KEY],
            1)

        #   Open text file, return string
        #
        metadata2 = self.job_01_text.get_metadata(as_string=True)
        #   print('type(metadata2.result_obj)', type(metadata2.result_obj))

        self.assertTrue(metadata2.success)

        str_to_find1 = '"%s": 6610' % col_const.DATASET_ROW_CNT
        self.assertTrue(metadata2.result_obj.find(str_to_find1) > -1)

        str_to_find2 = '"%s": 1' % col_const.VERSION_KEY
        self.assertTrue(metadata2.result_obj.find(str_to_find2) > -1)

        # Check the info from the MetadataUpdate
        #
        metadata_01_obj = self.get_metadata_obj(self.job_01_text)
        metadata_info = metadata_01_obj.get_metadata()
        self.assertTrue(metadata_info.success)

        metadata_dict = metadata_info.result_obj
        self.assertEqual(\
            metadata_dict[col_const.DATASET_LEVEL_KEY][col_const.DATASET_ROW_CNT],
            6610)

        self.assertEqual(\
            metadata_dict[col_const.VARIABLES_SECTION_KEY]['ccode'][col_const.DESCRIPTION_LABEL],
            self.code_book_description)

        self.assertEqual(\
            metadata_dict[col_const.SELF_SECTION_KEY][col_const.VERSION_KEY],
            2)

        # clean up
        #
        self.delete_metadata_files(metadata_01_obj.orig_metadata.id)
        #   metadata_01_obj.metadata_file.delete()

    #   @skip('skipit')
    def test_20_get_metata(self):
        """Read metadata that has (we think) bytes file encoding"""
        msgt(self.test_20_get_metata.__doc__)

        # Open bytes file, return dict
        #
        metadata3 = self.job_02_binary.get_metadata()
        #   print('type(metadata3.result_obj)', type(metadata3.result_obj))

        self.assertTrue(metadata3.success)
        self.assertEqual(metadata3.result_obj[col_const.DATASET_LEVEL_KEY][col_const.DATASET_ROW_CNT], 6610)
        self.assertEqual(metadata3.result_obj[col_const.SELF_SECTION_KEY][col_const.VERSION_KEY], 1)

        # Open bytes file, return string
        #
        metadata4 = self.job_02_binary.get_metadata(as_string=True)
        self.assertTrue(metadata4.success)

        str_to_find1 = '"%s": 6610' % col_const.DATASET_ROW_CNT
        self.assertTrue(metadata4.result_obj.find(str_to_find1) > -1)

        return
        # Create a MetadataUpdate and delete its file
        #
        metadata_02_obj = self.get_metadata_obj(self.job_02_binary)
        metadata_02_obj.metadata_file.delete()
        metadata_info = metadata_02_obj.get_metadata()
        self.assertTrue(metadata_info.success is False)

        # Clean up test files
        #
        self.delete_metadata_files(metadata_02_obj.orig_metadata.id)

    #   @skip('skipit')
    def test_30_multi_version_updates(self):
        """Make sure minor/major versions are correct"""
        msgt(self.test_30_multi_version_updates.__doc__)

        # Open text file, return dict
        #
        metadata = self.job_01_text.get_metadata()
        self.assertTrue(metadata.success)
        self.assertEqual(metadata.result_obj['self']['version'], 1)

        # Check the info from the MetadataUpdate
        #
        metadata_01_obj = self.get_metadata_obj(self.job_01_text)
        metadata_info = metadata_01_obj.get_metadata()
        self.assertTrue(metadata_info.success)
        metadata_dict = metadata_info.result_obj
        self.assertEqual(metadata_dict['self']['version'], 2)

        # minor version update: 2.1
        #
        metadata_obj = self.get_metadata_obj(
                                self.job_01_text,
                                viewable=False)
        new_version = Decimal('2.1')
        self.assertEqual(metadata_obj.version_number, new_version)
        self.assertEqual(metadata_obj.version_number, new_version)
        metadata_info = metadata_obj.get_metadata()
        self.assertEqual(metadata_info.result_obj['self']['version'],
                         new_version)

        # minor version update: 2.2
        #
        metadata_obj = self.get_metadata_obj(
                                self.job_01_text,
                                omit_list=['median'])
        new_version = Decimal('2.2')
        self.assertEqual(metadata_obj.version_number, new_version)
        metadata_info = metadata_obj.get_metadata()
        self.assertEqual(metadata_info.result_obj['self']['version'],
                         new_version)

        # major version update: 3
        #
        labl_code_book = 'code book 3'
        metadata_obj = self.get_metadata_obj(
                                self.job_01_text,
                                description=labl_code_book)
        new_version = Decimal('3')
        self.assertEqual(metadata_obj.version_number, new_version)
        metadata_info = metadata_obj.get_metadata()
        self.assertEqual(metadata_info.result_obj['self']['version'],
                         new_version)

        # minor version update: 3.1
        #
        metadata_obj = self.get_metadata_obj(
                                self.job_01_text,
                                description=labl_code_book,
                                omit_list=[])
        new_version = Decimal('3.1')
        self.assertEqual(metadata_obj.version_number, new_version)
        metadata_info = metadata_obj.get_metadata()
        self.assertEqual(metadata_info.result_obj['self']['version'],
                         new_version)

        # major version update: 4  (major + minor changes)
        #
        metadata_obj = self.get_metadata_obj(
                                self.job_01_text,
                                description='code book 4',
                                omit_list=['median', 'mean'])
        new_version = Decimal(4)
        self.assertEqual(metadata_obj.version_number, new_version)
        metadata_info = metadata_obj.get_metadata()
        self.assertEqual(metadata_info.result_obj['self']['version'],
                         new_version)

        # Clean up test files
        #
        self.delete_metadata_files(metadata_obj.orig_metadata.id)
