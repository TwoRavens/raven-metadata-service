import json
import decimal
from os.path import basename
from collections import OrderedDict
from django.urls import reverse
from django.db import models
from django.conf import settings
from django.utils.safestring import mark_safe

import jsonfield
from model_utils.models import TimeStampedModel
from ravens_metadata_apps.raven_auth.models import User
from ravens_metadata_apps.utils.json_util import json_dump


STATE_RECEIVED = u'RECEIVED'
STATE_PENDING = u'PENDING'
STATE_DATA_RETRIEVED = u'DATA_RETRIEVED'
STATE_PREPROCESS_STARTED = u'PREPROCESS_STARTED'
STATE_SUCCESS = u'SUCCESS'
STATE_FAILURE = u'FAILURE'
STATE_REVOKED = u'REVOKED'

PREPROCESS_STATES = (STATE_RECEIVED,
                     STATE_PENDING,
                     STATE_DATA_RETRIEVED,
                     STATE_PREPROCESS_STARTED,
                     STATE_SUCCESS,
                     STATE_FAILURE)
                     #STATE_REVOKED)

PREPROCESS_CHOICES = [(x, x) for x in PREPROCESS_STATES]

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
                    help_text='Source file for preprocess',
                    upload_to='source_file/%Y/%m/%d/',
                    blank=True)

    preprocess_file = models.FileField(\
                    help_text='Summary metadata created by preprocess',
                    upload_to='preprocess_file/%Y/%m/%d/',
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

    def __str__(self):
        """minimal, change to name"""
        return self.name

    def save(self, *args, **kwargs):
        """update name..."""
        if not self.id:
            super(PreprocessJob, self).save(*args, **kwargs)

        self.name = basename(self.source_file.name)[:100]

        if self.state == STATE_SUCCESS:
            self.is_success = True
        else:
            self.is_success = False

        super(PreprocessJob, self).save(*args, **kwargs)

    def as_dict(self):
        """return info dict"""
        od = OrderedDict()

        for attr_name in self.__dict__.keys():
            if attr_name.startswith('_'):
                continue

            elif attr_name == 'creator_id':
                if self.creator:
                    creator_info = self.creator.as_dict_short()
                    od['creator'] = creator_info
                else:
                    od['creator'] = None
            else:
                od[attr_name] = '%s' % self.__dict__[attr_name]


        if self.preprocess_file:
            data_ok, data_or_err = self.get_metadata()
            if data_ok:
                od['data'] = data_or_err
            else:
                od['data'] = 'ERROR: %s' % data_or_err

        return od

    def get_version_string(self):
        """Always 1"""
        return "1.0"

    def get_download_preprocess_url(self):
        """Get the download url"""
        reverse('api_get_latest_metadata',
                kwargs=dict(preprocess_id=self.id))

    def get_metadata_as_json(self):
        """For display, return preprocess file as string if it exists"""
        success, info = self.get_metadata(as_string=True)

        return info

    def get_preprocess_filesize(self):
        """Return the size of the file"""
        if self.preprocess_file:
            return self.preprocess_file.size

        return None

    def is_original_metadata(self):
        """This is the original, there is no previous metadata"""
        return True

    def get_metadata(self, as_string=False):
        """Return preprocess file contents if they exist"""

        if not self.preprocess_file:
            return False, 'No preprocess data. e.g. No file'

        try:
            self.preprocess_file.open(mode='r')
            file_data = self.preprocess_file.read()
            self.preprocess_file.close()
        except FileNotFoundError:
            return False, 'Preprocess file not found for job id: %s' % self.id

        try:
            json_dict = json.loads(file_data,
                                   object_pairs_hook=OrderedDict,
                                   parse_float=decimal.Decimal)
        except ValueError:
            return False, 'File contained invalid JSON! (%s)' % (self.preprocess_file)

        if as_string:
            return json_dump(json_dict, indent=4)

        return True, json_dict


    def get_absolute_url(self):
        """jobs status..."""
        return self.get_job_status_link()


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
            return self.source_file.path

        return 'n/a'

    def is_tab_source_file(self):
        """Is the source file a .tab file"""
        if self.source_file:
            if self.source_file.path.lower().endswith('.tab'):
                return True
        return False

    def is_csv_source_file(self):
        """Is the source file a .tab file"""
        if self.source_file:
            if self.source_file.path.lower().endswith('.csv'):
                return True
        return False

    def is_finished(self):
        """Is the task complete?"""
        return self.state in (STATE_SUCCESS, STATE_FAILURE)

    def has_error(self):
        """Was there an error?"""
        return self.state == STATE_FAILURE

    def set_state_data_retrieved(self):
        """set state to STATE_DATA_RETRIEVED"""
        self.state = STATE_DATA_RETRIEVED

    def set_state_preprocess_started(self):
        """set state to STATE_PREPROCESS_STARTED"""
        self.state = STATE_PREPROCESS_STARTED

    def set_state_success(self):
        """set state to STATE_SUCCESS"""
        self.state = STATE_SUCCESS

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
                    upload_to='preprocess_file/%Y/%m/%d/',
                    blank=True)

    editor = models.ForeignKey(User,
                               blank=True,
                               null=True,
                               on_delete=models.SET_NULL)

    note = models.TextField(blank=True)

    def get_version_string(self):
        """Return the version in string format"""
        # print("string version_number", str(self.version_number))
        # 3.0 => '3.0'
        return str(self.version_number)

    # def get_download_preprocess_version_url(self):
    #     """Get the download url"""
    #     reverse('api_get_metadata_version',
    #             kwargs=dict(preprocess_id=self.id,version=self.version_number))

    #def get_download_preprocess_url(self):
    #    """Get the download url"""
    #    reverse('api_get_latest_metadata',
    #            kwargs=dict(preprocess_id=self.id))


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

    def get_preprocess_filesize(self):
        """Return the size of the file"""
        if self.metadata_file:
            return self.metadata_file.size

        return None

    def save(self, *args, **kwargs):
        """update name..."""
        if not self.id:
            super(MetadataUpdate, self).save(*args, **kwargs)

        self.name = 'update %d' % self.id #basename(self.source_file.name)[:100]

        super(MetadataUpdate, self).save(*args, **kwargs)

    def get_metadata_as_json(self):
        """For display, return preprocess file as string if it exists"""
        success, info = self.get_metadata(as_string=True)

        return info


    def get_metadata(self, as_string=False):
        """Return preprocess file contents if they exist"""

        if not self.metadata_file:
            return False, 'No preprocess data. e.g. No file'

        try:
            file_data = self.metadata_file.read()
        except FileNotFoundError:
            return False, 'Metadata file not found for job id: %s' % self.id

        try:
            json_dict = json.loads(file_data,
                                   object_pairs_hook=OrderedDict,
                                   parse_float=decimal.Decimal)
        except ValueError:
            return False, 'File contained invalid JSON! (%s)' % (self.preprocess_file)

        if as_string:
            return json_dump(json_dict, indent=4)

        return True, json_dict

    def get_download_preprocess_url(self):
        """Get the download url"""
        return reverse('api_download_version',
                       kwargs=dict(preprocess_id=self.id,
                                   version=self.get_version_string()))
