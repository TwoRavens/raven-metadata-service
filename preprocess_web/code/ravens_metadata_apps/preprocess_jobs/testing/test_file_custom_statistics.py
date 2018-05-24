"""
Running individual tests

python manage.py test ravens_metadata_apps.preprocess_jobs.tests.test_file_encoding
"""
from os.path import abspath, dirname, isdir, isfile, join
import json
from decimal import Decimal
from unittest import skip
from collections import OrderedDict
from django.test import TestCase
from django.core.files.base import ContentFile
from django.template.loader import render_to_string

from msg_util import msgt
from ravens_metadata_apps.utils.view_helper import \
    (get_request_body_as_json,
     get_json_error,
     get_json_success,
     get_baseurl_from_request)
import col_info_constants as col_const
import update_constants as update_const

from ravens_metadata_apps.preprocess_jobs.models import PreprocessJob
from ravens_metadata_apps.utils.random_util import get_alphanumeric_lowercase
from ravens_metadata_apps.utils.time_util import get_timestring_for_file
from ravens_metadata_apps.preprocess_jobs.models import MetadataUpdate
from ravens_metadata_apps.preprocess_jobs.metadata_update_util import \
    (MetadataUpdateUtil)

TEST_FILE_DIR = join(dirname(abspath(__file__)), 'test_files')

class CustomStatisticsTestCases(TestCase):

    def setUp(self):
        """Set up PreprocessJobs"""
        self.code_book_description = "code book label"

        self.job_01_text = self.get_preprocess_job_with_file()

        self.job_02_binary = self.get_preprocess_job_with_file(as_binary=True)

        self.update_json ={
        col_const.PREPROCESS_ID:1,
        col_const.CUSTOM_KEY:[
            {
                "variables": [
                    "ccode"
                ],
                "image": [

                ],
                "name": "products",
                "value": "65555",
                "description": "product of numbers",
                "replication": "pi(n)"
            },
            {
                "variables": [
                    "country"
                ],
                "image": [

                ],
                "name": "products",
                "value": "6553225",
                "description": "product of numbers",
                "replication": "pi(n)"}]}


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

        #print('update_str', update_str)

        update_json = json.loads(update_str)

        # viewable for minor update
        update_json[update_const.VARIABLE_UPDATES]['ccode']['viewable'] = viewable
        update_json[update_const.VARIABLE_UPDATES]['ccode']['omit'] = omit_list
        update_json[update_const.VARIABLE_UPDATES]['ccode'][update_const.VALUE_UPDATES_KEY][col_const.DESCRIPTION_LABEL] = description

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

        preprocess_string = preprocess_string.encode("utf-8")
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


    def test_10_custom_statistics_add(self):
        """(10) test the custom_statistics add feature"""
        msgt(self.test_10_custom_statistics_add.__doc__)
        metadata_01_obj = self.get_metadata_obj(self.job_01_text)
        preprocess_id = metadata_01_obj.orig_metadata.id

        # check ID
        #
        self.assertEqual(preprocess_id,
                         self.update_json[col_const.PREPROCESS_ID],
                         "ID check passed")

        # get updated metadata
        #
        update_util = MetadataUpdateUtil(\
                        preprocess_id,
                        self.update_json[col_const.CUSTOM_KEY], col_const.UPDATE_CUSTOM_STATISTICS)
        # print(update_util.get_updated_metadata()['custom_statistics'])

        # check custom_statistics ID's
        #
        id_list = ['id_000001', 'id_000002']
        id_list_from_metadata = list(update_util.get_updated_metadata()[col_const.CUSTOM_KEY])
        # print(id_list_from_metadata)
        self.assertEqual(id_list,
                         id_list_from_metadata,
                         "Custom Statistics ID check passed")

        # value test
        #
        value = update_util.get_updated_metadata()[col_const.CUSTOM_KEY][id_list[0]]['value']
        # print(value)
        self.assertEqual(value, '65555')

    def test_20_custom_statistics_add_fail(self):
        """(20) test the custom stats error messages"""
        msgt(self.test_20_custom_statistics_add_fail.__doc__)
        update_json = {
            col_const.PREPROCESS_ID: 1,
            col_const.CUSTOM_KEY: [
                {
                    "variables": [
                        "mpg"
                    ],
                    "image": [

                    ],
                    "value": "65555",
                    "description": "product of numbers",
                    "replication": "pi(n)"
                }

            ]
        }

        """update_json has error for variables
            - mpg is not a variable name in metadata
              and produces a 'no name' error"""

        metadata_01_obj = self.get_metadata_obj(self.job_01_text)
        preprocess_id = metadata_01_obj.orig_metadata.id
        update_util = MetadataUpdateUtil(preprocess_id, update_json[col_const.CUSTOM_KEY],
                                         col_const.UPDATE_CUSTOM_STATISTICS)
        # error test
        #
        self.assertTrue(update_util.has_error)

    def test_30_custom_statistics_update(self):
        """(30) Test the update feature for custom stats"""
        msgt(self.test_30_custom_statistics_update.__doc__)
        update_json = {\
                  col_const.PREPROCESS_ID: 1,
                  col_const.CUSTOM_KEY: [\
                    {\
                      "id": "id_000001",
                      "updates": {\
                        "name": "Fourth order statistic",
                        "value": 80}},
                    {\
                      "id": "id_000002",
                      "updates": {\
                        "name": "third order statistic",
                        "value": 810,
                        "description": "new desc"}}]}

        metadata_01_obj = self.get_metadata_obj(self.job_01_text)
        preprocess_id = metadata_01_obj.orig_metadata.id
        add_util = MetadataUpdateUtil(\
                        preprocess_id,
                        self.update_json[col_const.CUSTOM_KEY],
                        col_const.UPDATE_CUSTOM_STATISTICS)
        id_list_from_metadata = list(add_util.get_updated_metadata()[col_const.CUSTOM_KEY])
        update_util = MetadataUpdateUtil(\
                            preprocess_id,
                            update_json[col_const.CUSTOM_KEY],
                            col_const.UPDATE_TO_CUSTOM_STATISTICS)

        #   name and desc test
        #
        name = update_util.get_updated_metadata()[col_const.CUSTOM_KEY][id_list_from_metadata[0]]['name']
        # print(value)
        self.assertEqual(name, 'Fourth order statistic')

        desc = update_util.get_updated_metadata()[col_const.CUSTOM_KEY][id_list_from_metadata[1]]['description']
        # print(value)
        self.assertEqual(desc, 'new desc')

    def test_40_custom_statistics_update_fail(self):
        """(40) Test update feature err checking for custom stats"""
        msgt(self.test_40_custom_statistics_update_fail.__doc__)
        update_json = {
            col_const.PREPROCESS_ID: 1,
            col_const.CUSTOM_KEY: [
                {
                    "id": "id_000005",
                    "updates": {
                        "name": "Fourth order statistic",
                        "value": 80
                    }
                },
                {
                    "id": "id_000002"
                }

            ]
        }
        metadata_01_obj = self.get_metadata_obj(self.job_01_text)
        preprocess_id = metadata_01_obj.orig_metadata.id
        MetadataUpdateUtil(preprocess_id,
                           self.update_json[col_const.CUSTOM_KEY],
                           col_const.UPDATE_CUSTOM_STATISTICS)

        # error check for wrong ID and key error [ ' updates' ]
        #
        update_util = MetadataUpdateUtil(preprocess_id, update_json[col_const.CUSTOM_KEY],
                                         col_const.UPDATE_TO_CUSTOM_STATISTICS)

        self.assertTrue(update_util.has_error)

    def test_50_custom_statistics_delete(self):
        """(50) custom stats delete"""
        msgt(self.test_50_custom_statistics_delete.__doc__)
        update_json = {\
               col_const.PREPROCESS_ID: 1,
               col_const.CUSTOM_KEY:[ \
                  { \
                     "id":"id_000001",
                     "delete": [\
                        "description",
                        "replication"]},
                  {\
                     "id": "id_000002",
                     "delete": [ \
                        "id"]}]}

        metadata_01_obj = self.get_metadata_obj(self.job_01_text)

        preprocess_id = metadata_01_obj.orig_metadata.id

        add_util = MetadataUpdateUtil(\
                            preprocess_id,
                            self.update_json[col_const.CUSTOM_KEY],
                            col_const.UPDATE_CUSTOM_STATISTICS)

        id_list_from_metadata = list(add_util.get_updated_metadata()[col_const.CUSTOM_KEY])

        delete_util = MetadataUpdateUtil(preprocess_id, update_json[col_const.CUSTOM_KEY],
                                         col_const.DELETE_CUSTOM_STATISTICS)

        # self.assertRaises(KeyError, delete_util.get_updated_metadata()[col_const.CUSTOM_KEY][id_list_from_metadata[1]])


    def test_60_custom_statistics_delete_fail(self):
        """(60) custom stats delete fail"""
        msgt(self.test_60_custom_statistics_delete_fail.__doc__)
        update_json = {\
               col_const.PREPROCESS_ID: 1,
               col_const.CUSTOM_KEY:[\
                  {\
                     "id":"id_000001",
                     "delete": [\
                        "description",
                        "replication"]},\
                  {\
                     "id": "id_000003",
                     "delete": [\
                        "id"]}]}
        metadata_01_obj = self.get_metadata_obj(self.job_01_text)
        preprocess_id = metadata_01_obj.orig_metadata.id
        MetadataUpdateUtil(preprocess_id,
                           self.update_json[col_const.CUSTOM_KEY],
                           col_const.UPDATE_CUSTOM_STATISTICS)

        # error check for wrong ID key error [ 'id_000003' ]
        #
        update_util = MetadataUpdateUtil(\
                            preprocess_id,
                            update_json[col_const.CUSTOM_KEY],
                            col_const.DELETE_CUSTOM_STATISTICS)

        self.assertTrue(update_util.has_error)
