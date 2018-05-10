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


class CustomStatisticsTestCases(object):

    def setUp(self):
        """Set up PreprocessJobs"""
        self.code_book_description = "code book label"

        self.job_01_text = self.get_preprocess_job_with_file()

        self.job_02_binary = self.get_preprocess_job_with_file(as_binary=True)