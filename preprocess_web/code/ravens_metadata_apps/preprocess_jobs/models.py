import json
import decimal
from os.path import basename
from collections import OrderedDict
from django.urls import reverse
from django.db import models
from django.conf import settings
from django.utils.safestring import mark_safe
from django.utils.text import slugify
from distutils.util import strtobool
from django.utils import timezone

import jsonfield
from humanfriendly import format_timespan
from model_utils.models import TimeStampedModel

from file_format_util import TAB_FILE_EXT, CSV_FILE_EXT
from ravens_metadata_apps.raven_auth.models import User
from ravens_metadata_apps.utils.json_util import json_dump
from ravens_metadata_apps.utils.basic_response import \
    (ok_resp, err_resp)


STATE_RECEIVED = u'RECEIVED'
STATE_PENDING = u'PENDING'
STATE_RETRIEVING_DATA = u'STATE_RETRIEVING_DATA'
STATE_DATA_RETRIEVED = u'DATA_RETRIEVED'
STATE_PREPROCESS_STARTED = u'PREPROCESS_STARTED'
STATE_SUCCESS = u'SUCCESS'
STATE_FAILURE = u'FAILURE'
STATE_REVOKED = u'REVOKED'

PREPROCESS_STATES = (STATE_RECEIVED,
                     STATE_PENDING,
                     STATE_RETRIEVING_DATA,
                     STATE_DATA_RETRIEVED,
                     STATE_PREPROCESS_STARTED,
                     STATE_SUCCESS,
                     STATE_FAILURE)
                     #STATE_REVOKED)

PREPROCESS_CHOICES = [(x, x) for x in PREPROCESS_STATES]

NOT_IMPLEMENTED_FOR_OBJECT_STORAGE = ('Not implemented for object storage'
                                      ' (e.g AWS S3, Google Buckets, etc)')

class PreprocessJob(TimeStampedModel):
    """Initial, minimal model"""
    name = models.CharField(max_length=255,
                            blank=True)

    is_metadata_public = models.BooleanField(default=True)

    creator = models.ForeignKey(User,
                                blank=True,
                                null=True,
                                on_delete=models.SET_NULL)

    state = models.CharField(max_length=100,
                             choices=PREPROCESS_CHOICES,
                             default=STATE_RECEIVED)

    is_success = models.BooleanField(default=False)

    task_id = models.CharField('queue task id (e.g. celery id)',
                               max_length=255,
                               blank=True)

    source_file_url = models.URLField(\
                    'direct download url (optional)',
                    blank=True)

    source_file = models.FileField(\
                    help_text='Source file to analyze',
                    upload_to='source_file/%Y/%m/%d/',
                    blank=True)

    metadata_file = models.FileField(\
                    help_text='Summary metadata created by preprocess',
                    upload_to='metadata_file/%Y/%m/%d/',
                    blank=True)

    schema_version = models.CharField(max_length=100,
                                      default='beta')

    end_time = models.DateTimeField(blank=True, null=True)

    user_message = models.TextField(\
                blank=True,
                help_text='May be used for error messages, etc')


    class Meta:
        permissions = (
            ('view_preprocess_job', 'View Preprocess Job'),
            #('view_preprocess_job', 'View PreprocessJob'),
        )
        ordering = ('-created',)

    def __str__(self):
        """minimal, change to name"""
        return self.name

    def save(self, *args, **kwargs):
        """update name..."""
        if not self.id:
            super(PreprocessJob, self).save(*args, **kwargs)

        if not self.name:
            if self.source_file:
                self.name = basename(self.source_file.name)[:100]
            else:
                self.name = 'job %s' % self.id

        if self.state == STATE_SUCCESS:
            self.is_success = True
        else:
            self.is_success = False

        super(PreprocessJob, self).save(*args, **kwargs)

    def as_dict(self):
        """return info dict"""
        od = OrderedDict()

        for attr_name in self.__dict__.keys():

            # check for attributes to skip...
            if attr_name.startswith('_'):
                continue

            val = self.__dict__[attr_name]
            if isinstance(val, models.fields.files.FieldFile):
                # this is a file field...
                #
                val = str(val)  # file path or empty string
                if val == '':
                    val = None
                od[attr_name] = val

            elif attr_name == 'creator_id':
                # user details...
                #
                if self.creator:
                    creator_info = self.creator.as_dict_short()
                    od['creator'] = creator_info
                else:
                    od['creator'] = None
            else:
                od[attr_name] = val

        # Add the metadata file contents, if they exist
        #
        if self.metadata_file:
            data_ok, data_or_err = self.get_metadata()
            if data_ok:
                od['summary_metadata'] = data_or_err
            else:
                od['summary_metadata'] = 'ERROR: %s' % data_or_err

        return od

    def get_version_string(self, as_slug=False):
        """Always 1"""
        if as_slug:
            return "1-0"

        return "1.0"

    def get_download_preprocess_url(self):
        """Get the download url"""
        reverse('api_get_latest_metadata',
                kwargs=dict(preprocess_id=self.id))

    def get_metadata_as_json(self):
        """For display, return preprocess file as string if it exists"""
        success, info = self.get_metadata(as_string=True)

        return info

    def get_metadata_filesize(self):
        """Return the size of the preprocess file"""
        if self.metadata_file:
            return self.metadata_file.size

        return None


    def get_source_filesize(self):
        """Return the size of the source file"""
        if self.source_file:
            return self.source_file.size

        return None

    def get_elapsed_time(self):
        """Return the time needed to run preprocess"""
        if not self.end_time:
            return None

        elapsed_time = self.end_time - self.created

        return format_timespan(elapsed_time.total_seconds())


    def is_original_metadata(self):
        """This is the original, there is no previous metadata"""
        return True

    def get_metadata(self, as_string=False):
        """Return preprocess file contents if they exist"""
        if not self.metadata_file:
            return err_resp('No preprocess data. e.g. No file')

        try:
            self.metadata_file.open(mode='r')
            file_data = self.metadata_file.read()
            self.metadata_file.close()
        except FileNotFoundError:
            return err_resp('Metadata file not found for job id: %s' % \
                            self.id)

        if isinstance(file_data, bytes): #type(file_data) is bytes:
            #print('BYTES found!')
            file_data = file_data.decode('utf-8')

        try:
            json_dict = json.loads(file_data,
                                   object_pairs_hook=OrderedDict,
                                   parse_float=decimal.Decimal)
        except ValueError:
            return err_resp('File contained invalid JSON! (%s)' % \
                            (self.metadata_file))

        if as_string:
            return json_dump(json_dict, indent=4)

        return ok_resp(json_dict)


    def get_absolute_url(self):
        """jobs status..."""
        return reverse('view_job_versions',
                       kwargs=dict(preprocess_id=self.id))
        #return self.get_job_status_link()

    def get_preprocess_id(self):
        """Return the id of the preprocess job"""
        if self.id:
            return self.id

        return None

    def get_job_status_link(self, base_url=''):
        """for callbacks to check status and/or get preprocess data"""
        #if not base_url:
        #    base_url = 'http://127.0.0.1:8000'

        status_url = reverse('show_job_info',
                             kwargs=dict(job_id=self.id))

        return '%s%s' % (base_url, status_url)

    def source_file_path(self):
        """To display the full path in the admin"""

        if self.source_file:
            try:
                return ok_resp(self.source_file.path)
            except NotImplementedError:
                return err_resp(NOT_IMPLEMENTED_FOR_OBJECT_STORAGE)
        return err_resp('The "source_file" is not set')

    def source_filename(self):
        """return the source filename (basename only)"""
        if self.source_file:
            return basename(self.source_file.name)

        return '(no source file)'

    def metadata_filename(self):
        """return the preprocess filename (basename only)"""
        if self.metadata_file:
            return basename(self.metadata_file.name)

        return '(no preprocess file)'

    def is_tab_source_file(self):
        """Is the source file a .tab file"""
        if self.source_file:
            if self.source_file.name.lower().endswith(TAB_FILE_EXT):
                return True
        return False

    def is_csv_source_file(self):
        """Is the source file a .FORMAT_CSV file"""
        if self.source_file:
            if self.source_file.name.lower().endswith(CSV_FILE_EXT):
                return True
        return False

    def is_finished(self):
        """Is the task complete?"""
        return self.state in (STATE_SUCCESS, STATE_FAILURE)

    def has_error(self):
        """Was there an error?"""
        return self.state == STATE_FAILURE

    def set_state_pending(self):
        """set state to STATE_PENDING"""
        self.state = STATE_PENDING

    def set_state_retrieving_data(self):
        """set state to STATE_RETRIEVING_DATA"""
        self.state = STATE_RETRIEVING_DATA

    def set_state_data_retrieved(self):
        """set state to STATE_DATA_RETRIEVED"""
        self.state = STATE_DATA_RETRIEVED

    def set_state_preprocess_started(self):
        """set state to STATE_PREPROCESS_STARTED"""
        self.state = STATE_PREPROCESS_STARTED

    def set_state_success(self):
        """set state to STATE_SUCCESS"""
        self.state = STATE_SUCCESS
        self.end_time = timezone.now()

    def set_state_failure(self, user_msg=None):
        """set state to STATE_FAILURE"""
        self.state = STATE_FAILURE
        if user_msg:
            self.user_message = user_msg

    def get_latest_preprocess_url(self):
        """Get the download url"""
        reverse('api_get_latest_metadata',
                kwargs=dict(preprocess_id=self.id))

    def get_download_preprocess_url(self):
         """Get the download url"""
         return reverse('api_download_version',
                        kwargs=dict(preprocess_id=self.id,
                                    version=self.get_version_string()))


class MetadataUpdate(TimeStampedModel):
    """Track updates to preprocss metadata"""
    name = models.CharField(max_length=255,
                            blank=True)

    previous_update = models.ForeignKey('self',
                                        on_delete=models.PROTECT,
                                        blank=True,
                                        null=True,
                                        related_name='prev_metadata')

    orig_metadata = models.ForeignKey(PreprocessJob,
                                      on_delete=models.PROTECT,
                                      related_name='orig_metadata')

    version_number = models.DecimalField(default=2,
                                         max_digits=8,
                                         decimal_places=1)

    update_json = jsonfield.JSONField(\
                    load_kwargs=dict(object_pairs_hook=OrderedDict))

    metadata_file = models.FileField(\
                    help_text='Summary metadata created by preprocess',
                    upload_to='metadata_file/%Y/%m/%d/',
                    blank=True)

    editor = models.ForeignKey(User,
                               blank=True,
                               null=True,
                               on_delete=models.SET_NULL)

    note = models.TextField(blank=True)

    def get_version_string(self, as_slug=False):
        """Return the version in string format"""
        # print("string version_number", str(self.version_number))
        # 3.0 => '3.0'
        if as_slug:
            return slugify(str(self.version_number))

        return str(self.version_number)


    def __str__(self):
        """minimal, change to name"""
        return self.name


    class Meta:
        ordering = ('-created',)
        unique_together = ('orig_metadata', 'version_number')

    def is_original_metadata(self):
        """This is the original, there is no previous metadata"""
        return False

    def metadata_file_path(self):
        """To display the full path in the admin"""
        if self.metadata_file:
            return self.metadata_file.path

        return 'n/a'

    def update_data_as_json(self):
        """Return preprocess file contents if they exist"""
        if self.update_json:
            json_info = json_dump(self.update_json, indent=4)
            if json_info.success:
                return mark_safe('<pre>%s</pre>' % json_info.result_obj)

            return json_info.err_msg

        return None

    def get_metadata_filesize(self):
        """Return the size of the file"""
        if self.metadata_file:
                return self.metadata_file.size

        return None

    def save(self, *args, **kwargs):
        """update name..."""
        if not self.id:
            super(MetadataUpdate, self).save(*args, **kwargs)

        if self.orig_metadata:
            self.name = '%s (v%s)' % (self.orig_metadata.name,
                                    self.get_version_string())
        else:
            self.name = 'update %d' % self.get_version_string()
        ##basename(self.source_file.name)[:100]

        super(MetadataUpdate, self).save(*args, **kwargs)

    def get_metadata_as_json(self):
        """For display, return preprocess file as string if it exists"""
        success, info = self.get_metadata(as_string=True)

        return info

    def get_preprocess_id(self):
        """Return the id of the preprocess job"""
        if self.orig_metadata:
            return self.orig_metadata.id

        return None

    def get_metadata(self, as_string=False):
        """Return preprocess file contents if they exist"""

        if not self.metadata_file:
            return err_resp('No preprocess data. e.g. No file')

        try:
            self.metadata_file.open(mode='r')
            file_data = self.metadata_file.read()
            self.metadata_file.close()
        except FileNotFoundError:
            return err_resp('Metadata file not found for job id: %s' % self.id)

        if isinstance(file_data, bytes):
            file_data = file_data.decode('utf-8')

        try:
            json_dict = json.loads(file_data,
                                   object_pairs_hook=OrderedDict,
                                   parse_float=decimal.Decimal)
        except ValueError:
            return err_resp('File contained invalid JSON! (%s)' % \
                            (self.metadata_file))

        if as_string:
            return json_dump(json_dict, indent=4)

        return ok_resp(json_dict)

    def get_download_preprocess_url(self):
        """Get the download url"""
        return reverse('api_download_version',
                       kwargs=dict(preprocess_id=self.id,
                                   version=self.get_version_string()))
