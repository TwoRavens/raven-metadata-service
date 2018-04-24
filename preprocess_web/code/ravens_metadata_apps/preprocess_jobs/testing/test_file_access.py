"""
Running individual tests

python manage.py test ravens_metadata_apps.preprocess_jobs.tests.test_file_encoding
"""
from os.path import abspath, dirname, isdir, isfile, join
import json

from django.test import TestCase
from django.core.files.base import ContentFile
from django.template.loader import render_to_string

from msg_util import msgt

from ravens_metadata_apps.preprocess_jobs.models import PreprocessJob
from ravens_metadata_apps.utils.random_util import get_alphanumeric_lowercase
from ravens_metadata_apps.utils.time_util import get_timestring_for_file
from ravens_metadata_apps.preprocess_jobs.metadata_update_util import \
    (MetadataUpdateUtil)

TEST_FILE_DIR = join(dirname(abspath(__file__)), 'test_files')

class FileEncodingTestCase(TestCase):

    def setUp(self):
        """Set up PreprocessJobs"""
        self.code_book_label = "code book label"

        self.job_01_text = self.get_preprocess_job_with_file()

        self.job_02_binary = self.get_preprocess_job_with_file(as_binary=True)


    def tearDown(self):
        """Set up PreprocessJobs"""
        print('    - remove test files')
        self.job_01_text.metadata_file.delete()
        self.job_02_binary.metadata_file.delete()


    def get_metadata_obj(self, job_obj):
        """Create a new Metadata object using a PreprocessJob"""
        update_str = """{
                       "preprocess_id": %s,
                       "variable_updates":{
                          "ccode":{
                             "viewable":true,
                             "omit":[
                                "mean",
                                "median"
                             ],
                             "value_updates":{
                                "labl":"%s"
                             }
                          }
                       }
                    }""" % (job_obj.id, self.code_book_label)
        update_json = json.loads(update_str)

        update_util = MetadataUpdateUtil(job_obj.id, update_json)

        assert update_util.has_error is False,\
            "There shouldn't be an error!"

        return update_util.get_updated_metadata(as_obj=True)


    def get_preprocess_job_with_file(self, as_binary=False):
        """Create a new PreprocessJob with a preprocess_file"""
        kwargs = dict(name='job 01')
        ye_job = PreprocessJob(**kwargs)
        ye_job.save()

        preprocess_string = render_to_string(\
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

        #print('    - create test file:', ye_job.metadata_file.path)

        ye_job.set_state_success()
        ye_job.save()

        return ye_job



    def test_10_get_metata(self):
        """Read metadata that has a text file encoding"""
        msgt(self.test_10_get_metata.__doc__)

        # Open text file, return dict
        #
        metadata = self.job_01_text.get_metadata()
        #print('type(metadata.result_obj)', type(metadata.result_obj))
        self.assertTrue(metadata.success)
        self.assertEqual(metadata.result_obj['dataset']['row_cnt'], 6610)


        # Open text file, return string
        #
        metadata2 = self.job_01_text.get_metadata(as_string=True)
        #print('type(metadata2.result_obj)', type(metadata2.result_obj))

        self.assertTrue(metadata2.success)
        self.assertTrue(metadata2.result_obj.find('"row_cnt": 6610') > -1)


        # Check the info from the MetadataUpdate
        #
        metadata_01_obj = self.get_metadata_obj(self.job_01_text)
        metadata_info = metadata_01_obj.get_metadata()
        self.assertTrue(metadata_info.success)
        metadata_dict = metadata_info.result_obj
        self.assertEqual(metadata_dict['dataset']['row_cnt'], 6610)
        self.assertEqual(metadata_dict['variables']['ccode']["labl"],
                         self.code_book_label)

        # clean up
        #
        metadata_01_obj.metadata_file.delete()


    def test_20_get_metata(self):
        """Read metadata that has (we think) bytes file encoding"""
        msgt(self.test_20_get_metata.__doc__)

        # Open bytes file, return dict
        #
        metadata3 = self.job_02_binary.get_metadata()
        #print('type(metadata3.result_obj)', type(metadata3.result_obj))

        self.assertTrue(metadata3.success)
        self.assertEqual(metadata3.result_obj['dataset']['row_cnt'], 6610)

        # Open bytes file, return string
        #
        metadata4 = self.job_02_binary.get_metadata(as_string=True)
        self.assertTrue(metadata4.success)
        self.assertTrue(metadata4.result_obj.find('"row_cnt": 6610') > -1)

        # Create a MetadataUpdate and delete its file
        #
        metadata_02_obj = self.get_metadata_obj(self.job_02_binary)

        metadata_02_obj.metadata_file.delete()
        metadata_info = metadata_02_obj.get_metadata()
        self.assertTrue(metadata_info.success is False)
