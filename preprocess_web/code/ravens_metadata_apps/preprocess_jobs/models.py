import json
from collections import OrderedDict
from django.urls import reverse
from django.db import models
from django.conf import settings
from model_utils.models import TimeStampedModel
from ravens_metadata_apps.raven_auth.models import User
from os.path import basename


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
            file_data = self.preprocess_file.read()
            od['data'] = json.loads(file_data)

        return od

    def get_preprocess_data_as_json(self):
        """Return preprocess file contents if they exist"""
        if self.preprocess_file:
            file_data = self.preprocess_file.read()
            json_data = json.loads(file_data)
            return json.dumps(json_data, indent=4)

        return None

    def get_preprocess_data(self):
        """Return preprocess file contents if they exist"""
        if self.preprocess_file:
            file_data = self.preprocess_file.read()
            return json.loads(file_data)

        return None

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

    def set_state_failure(self):
        """set state to STATE_FAILURE"""
        self.state = STATE_FAILURE
