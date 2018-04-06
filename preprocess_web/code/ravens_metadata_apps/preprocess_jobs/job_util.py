"""Utility class for the preprocess workflow"""
import json, uuid
import pandas as pd
from collections import OrderedDict
from datetime import datetime as dt
from django.core.files.base import ContentFile
from django.http import HttpResponse
from django.utils import timezone
from .forms import FORMAT_JSON, FORMAT_CSV
from celery.result import AsyncResult
from preprocess_runner import PreprocessRunner
#from basic_preprocess import preprocess_csv_file
from ravens_metadata_apps.preprocess_jobs.tasks  import preprocess_csv_file,get_variable_display
from ravens_metadata_apps.utils.random_util import get_alphanumeric_lowercase
#from variable_display_util import VariableDisplayUtil
from ravens_metadata_apps.preprocess_jobs.models import \
    (PreprocessJob, MetadataUpdate,
     STATE_SUCCESS, STATE_FAILURE)


class JobUtil(object):
    """Convenience class for the preprocess work flow"""


    @staticmethod
    def get_latest_metadata(job_id):
        """Return the latest version of the metadata as an OrderedDict"""

        # Get the PreprocessJob or MetadataUpdate
        #
        success, obj_or_err = JobUtil.get_latest_metadata_object(job_id)
        if success is False:
            return False, obj_or_err


        print('type(obj_or_err)', type(obj_or_err))
        print('obj_or_err.id', obj_or_err.id)
        # Return the actual metadata as an OrderedDict
        #
        metadata_ok, metadata_or_err = obj_or_err.get_metadata()
        if metadata_ok is False:
            return False, metadata_or_err

        return True, metadata_or_err

    @staticmethod
    def get_version_metadata_object(job_id,version):
        """ Retrun the versions and detail of job"""
        if not job_id:
            return False, 'job_id cannot be None'
        if not version:
            return False, 'version cannot be None'

        update_object = MetadataUpdate.objects.filter(orig_metadata=job_id,version_number=version)
        if update_object:
            return True, update_object

        # Look for the original preprocess metadata
        #
        try:
            orig_metadata = PreprocessJob.objects.get(pk=job_id)
        except PreprocessJob.DoesNotExist:
            return False, 'PreprocessJob not found: %s' % job_id

        return True, orig_metadata


    @staticmethod
    def get_versions_metadata_objects(job_id):
        """ Retrun the versions and detail of job"""
        if not job_id:
            return False,'job_id cannot be None'

        update_objects = MetadataUpdate.objects.filter(orig_metadata=job_id)
        if update_objects:
            return True, update_objects

        # Look for the original preprocess metadata
        #
        try:
            orig_metadata = PreprocessJob.objects.get(pk=job_id)
        except PreprocessJob.DoesNotExist:
            return False, 'PreprocessJob not found: %s' % job_id

        return True, orig_metadata


    @staticmethod
    def get_latest_metadata_object(job_id):
        """Return either a PreprocessJob object (orig) or MetadataUpdate object (update)"""
        if not job_id:
            return False, 'job_id cannot be None'

        # Look for the latest update, if it exists
        #
        latest_update = MetadataUpdate.objects.filter(orig_metadata=job_id\
                                    ).order_by('-version_number'\
                                    ).first()

        # It exists! Return it
        #
        if latest_update:
            return True, latest_update

        # Look for the original preprocess metadata
        #
        try:
            orig_metadata = PreprocessJob.objects.get(pk=job_id)
        except PreprocessJob.DoesNotExist:
            return False, 'PreprocessJob not found: %s' % job_id

        return True, orig_metadata



    @staticmethod
    def start_preprocess(job):
        """Start the preprocessing!"""
        assert isinstance(job, PreprocessJob),\
               'job must be a PreprocessJob'

        # job_id = uuid.UUID.time

        # send the file to the queue
        task = preprocess_csv_file.delay(job.source_file.path, job_id=job.id)

        # set the task_id
        job.task_id = task.id

        # update the state of the job
        job.set_state_preprocess_started()

        # save the new state
        job.save()

    @staticmethod
    def check_status(job):
        """Check/update the job status"""
        assert isinstance(job, PreprocessJob),\
               'job must be a PreprocessJob'

        if job.is_finished():
            return

        ye_task = AsyncResult(job.task_id,
                              app=preprocess_csv_file)

        if ye_task.state == 'SUCCESS':

            preprocess_data = ContentFile(json.dumps(ye_task.result['data']))

            new_name = 'preprocess_%s.json' % get_alphanumeric_lowercase(8)
            job.preprocess_file.save(new_name,
                                     preprocess_data)
            job.set_state_success()

            job.user_message = 'Task completed!  Preprocess is available'
            job.end_time = timezone.now()
            job.save()
            ye_task.forget()

        elif ye_task.state == 'STATE_FAILURE':
            job.set_state_failure()
            job.user_message = 'ye_task failed....'
            job.save()
            #get_ok_resp('looking good: %s' % (ye_task.result['input_file']),
            #            data=ye_task.result['data']))

            # delete task!

    @staticmethod
    def retrieve_rows_json(job, **kwargs):

        print('kwargs', kwargs)
        start_row = kwargs.get('start_row')
        num_rows = kwargs.get('number_rows')
        input_format = kwargs.get('format')
        job_id = kwargs.get('preprocess_id')

        if job.is_tab_source_file():
            csv_data = pd.read_csv(job.source_file.path, sep='\t', lineterminator='\r')
            print(csv_data)
        elif job.is_csv_source_file():
            csv_data = pd.read_csv(job.source_file.path)
        else:
            return dict(success=True,
                        message='File type unknown (not csv or tab)')

        max_rows = len(csv_data)
        print("the no. of rows are ", max_rows)

        error_message = []

        if start_row > max_rows:
            err = 'The request was from %s rows but only %d rows were found, so default start rows = 1 is set' % (start_row, max_rows)
            error_message.append(err)
            start_row = 1
        elif num_rows > max_rows:
            err = 'The request was for %s rows but only %d rows were found, so number rows is set to max rows' % (num_rows, max_rows)
            error_message.append(err)
            num_rows = max_rows
        update_end_num = start_row + num_rows
        print("error message", error_message)
        data_frame = csv_data[start_row:update_end_num]
        raw_data = data_frame.to_dict(orient='split')

        # print("raw_data", raw_data)

        if len(error_message) > 0:
            output = {
                "success": True,
                "message": 'It worked but with some changes',
                "modifications": error_message,
                "attributes": {
                    "preprocess_id": job_id,
                    "start_row": start_row,
                    "num_rows": num_rows,
                    "format": input_format
                },
                "data": str(raw_data),
            }

        else:
            output = {
                "success": True,
                "message": 'It worked',
                "attributes": {
                    "preprocess_id": job_id,
                    "start_row": start_row,
                    "num_rows": num_rows,
                    "format": input_format
                },
                "data": str(raw_data),
            }

        return output

    @staticmethod
    def retrieve_rows_csv(request, job, **kwargs):
        if request.method == 'POST':
            print('kwargs', kwargs)
            start_row = kwargs.get('start_row')
            num_rows = kwargs.get('number_rows')
            if job.name.lower().endswith('.tab'):
                print("is tab file")
                csv_data = pd.read_csv(job.source_file.path, sep='\t', lineterminator='\r')
                print(csv_data)
            else:
                csv_data = pd.read_csv(job.source_file.path)
            max_rows = len(csv_data)
            print("the no. of rows are ", max_rows)

            error_message = []

            if start_row > max_rows:
                err = 'The request was from %s rows but only %d rows were found, so default start rows = 1 is set' % (
                    start_row, max_rows)
                error_message.append(err)
                start_row = 1
            elif num_rows > max_rows:
                err = 'The request was for %s rows but only %d rows were found, so number rows is set to max rows' % (
                    num_rows, max_rows)
                error_message.append(err)
                num_rows = max_rows

            print("error message", error_message)
            update_end_num = start_row + num_rows
            data_frame = csv_data[start_row:update_end_num]
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename=TwoRavensResponse.csv'

            data_frame.to_csv(path_or_buf=response, sep=',', float_format='%.2f', index=False)

            return response

    @staticmethod
    def update_preprocess_metadata(preprocess_json, update_json,**kwargs):
        """To get the updated preprocess file from VariableDisplayUtil """
        # result = get_variable_display(preprocess_json,update_json, preprocess_id=preprocess_id)
        var_util = VariableDisplayUtil(preprocess_json, update_json)
        if var_util.has_error:
            return False, var_util.get_error_messages()

        return True, var_util.get_updated_metadata()
