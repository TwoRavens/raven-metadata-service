"""Utility class for the preprocess workflow"""
import pandas as pd
from django.http import HttpResponse
from ravens_metadata_apps.preprocess_jobs.tasks import \
    (preprocess_csv_file,)
from ravens_metadata_apps.utils.time_util import get_timestring_for_file
from ravens_metadata_apps.utils.basic_response import \
    (ok_resp, err_resp)
from ravens_metadata_apps.preprocess_jobs.models import \
    (PreprocessJob, MetadataUpdate)
from variable_display_util import VariableDisplayUtil


class JobUtil(object):
    """Convenience class for the preprocess work flow"""

    @staticmethod
    def get_preprocess_job_dict(preprocess_id):
        """Return a PreprocessJob to check its status"""
        try:
            ze_job = PreprocessJob.objects.get(pk=preprocess_id)
        except PreprocessJob.DoesNotExist:
            return err_resp('PreprocessJob not found: %d' % preprocess_id)

        return ok_resp(ze_job.as_dict())

    @staticmethod
    def get_completed_preprocess_job(job_id):
        """Return only a completed PreprocessJob"""
        try:
            return PreprocessJob.objects.get(pk=job_id,
                                             is_success=True)
        except PreprocessJob.DoesNotExist:
            return None

    @staticmethod
    def get_latest_metadata(job_id):
        """Return the latest version of the metadata as an OrderedDict"""

        # Get the PreprocessJob or MetadataUpdate
        #
        success, obj_or_err = JobUtil.get_latest_metadata_object(job_id)
        if success is False:
            return err_resp(obj_or_err)

        print('type(obj_or_err)', type(obj_or_err))
        print('obj_or_err.id', obj_or_err.id)
        # Return the actual metadata as an OrderedDict
        #
        metadata_ok, metadata_or_err = obj_or_err.get_metadata()
        if metadata_ok is False:
            return err_resp(metadata_or_err)

        return ok_resp(metadata_or_err)

    @staticmethod
    def get_version_metadata_object(job_id, version):
        """ Retrun the versions and detail of job"""
        if not job_id:
            return err_resp('job_id cannot be None')
        if not version:
            return err_resp('version cannot be None')

        update_object = MetadataUpdate.objects.filter(\
                                 orig_metadata=job_id,
                                 version_number=version
                                ).first()
        # print("here is the data",update_object.name.version_number)
        if update_object:
            return ok_resp(update_object)

        # Look for the original preprocess metadata
        #
        orig_metadata = None
        err_msg = 'PreprocessJob not found for id: %s' % job_id
        try:
            if int(version) == 1:
                orig_metadata = JobUtil.get_completed_preprocess_job(job_id)
        except ValueError:
            return err_resp(err_msg)

        if orig_metadata:
            return ok_resp(orig_metadata)

        return err_resp(err_msg)

    @staticmethod
    def get_versions_metadata_objects(job_id):
        """ Return the versions and detail of job"""
        if not job_id:
            return err_resp('job_id cannot be None')

        update_objects = MetadataUpdate.objects.filter(orig_metadata=job_id)

        if update_objects:
            # return True, update_objects
            update_objects = list(update_objects)
        else:
            update_objects = []

        # Look for the original preprocess metadata
        #
        orig_metadata = JobUtil.get_completed_preprocess_job(job_id)
        if not orig_metadata:
            return err_resp('PreprocessJob not found for id: %s' % job_id)

        update_objects.append(orig_metadata)

        return ok_resp(update_objects)

    @staticmethod
    def get_latest_metadata_object(job_id):
        """Return either a PreprocessJob object (orig) or MetadataUpdate object (update)"""
        if not job_id:
            return False, 'job_id cannot be None'

        # Look for the latest update, if it exists
        #
        latest_update = MetadataUpdate.objects.filter(orig_metadata=job_id,)\
                                    .order_by('-version_number')\
                                    .first()

        # It exists! Return it
        #
        if latest_update:
            return True, latest_update

        # Look for the original preprocess metadata
        #
        orig_metadata = JobUtil.get_completed_preprocess_job(job_id)
        if not orig_metadata:
            return False, 'PreprocessJob not found for id: %s' % job_id

        return True, orig_metadata

    @staticmethod
    def start_preprocess(job):
        """Start the preprocessing!"""
        assert isinstance(job, PreprocessJob), 'job must be a PreprocessJob'

        if not job.source_file.name:
            err_msg = 'The PreprocessJob source_file is not available'
            job.set_state_failure(err_msg)
            job.save()
            return

        # send the file to the queue
        task = preprocess_csv_file.delay(
                    job.source_file.path,
                    job_id=job.id)

        # set the task_id
        job.task_id = task.id

        # update the state of the job
        job.set_state_preprocess_started()

        # save the new state
        job.save()

    @staticmethod
    def retrieve_rows_json(job, **kwargs):
        """Open the original data file and return the rows in JSON format (python dict)"""

        # Assume this passed through the RetrieveRowsForm for validation
        #
        start_row = kwargs.get('start_row')
        num_rows = kwargs.get('number_rows')
        input_format = kwargs.get('format')
        job_id = kwargs.get('preprocess_id')

        # -------------------------------------------
        # Read partial file, set lines to skip, etc
        # -------------------------------------------
        start_row_idx = start_row - 1    # e.g. if start_row is 1, skip nothing
                                         # if start_row is 10, start on index

        if job.is_tab_source_file():
            try:
                csv_data = pd.read_csv(job.source_file.path,
                                       sep='\t',
                                       lineterminator='\r',
                                       skiprows=start_row_idx,
                                       nrows=num_rows)

            except ValueError:
                print(" not good value for the row start")
                csv_data = pd.read_csv(job.source_file.path,
                                       sep='\t',
                                       lineterminator='\r',
                                       skiprows=0,
                                       nrows=num_rows)
            print(csv_data)
        elif job.is_csv_source_file():
            try:
                csv_data = pd.read_csv(job.source_file.path,
                                       skiprows=start_row_idx,
                                       nrows=num_rows)
            except ValueError:
                print(" not good value for the row start")
                csv_data = pd.read_csv(job.source_file.path,
                                       skiprows=0,
                                       nrows=num_rows)
            print(csv_data)
        else:
            return dict(success=False,
                        message='File type unknown (not csv or tab)')

        max_rows = len(csv_data.index)
        print("the no. of rows are ", max_rows)

        error_message = []

        if start_row > max_rows:
            err = 'The request was from %s rows but only %d rows were found, so default start rows = 1 is set'\
                    % (start_row, max_rows)
            error_message.append(err)
            start_row = 1
            start_row_idx = start_row - 1
        if num_rows > max_rows:
            err = 'The request was for %s rows but only %d rows were found, so number rows is set to max rows'\
                    % (num_rows, max_rows)
            error_message.append(err)
            num_rows = max_rows

        update_end_num = start_row + num_rows
        print("error message", error_message)
        data_frame = csv_data[start_row_idx:update_end_num - 1]
        raw_data = data_frame.to_dict(orient='split')
        print("num_rows ", num_rows)
        if 'index' in raw_data:
            del raw_data['index']
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
                "data": raw_data,
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
                "data": raw_data,
            }

        return output

    @staticmethod
    def retrieve_rows_csv(request, job, **kwargs):
        """Return data rows as a .csv file."""
        if request.method == 'POST':
            print('kwargs', kwargs)
            start_row = kwargs.get('start_row')
            num_rows = kwargs.get('number_rows')

            # -------------------------------------------
            # Read partial file, set lines to skip, etc
            # -------------------------------------------
            start_row_idx = start_row - 1  # e.g. if start_row is 1, skip nothing
            # if start_row is 10, start on index

            if job.is_tab_source_file():
                try:
                    csv_data = pd.read_csv(job.source_file.path,
                                           sep='\t',
                                           lineterminator='\r',
                                           skiprows=start_row_idx,
                                           nrows=num_rows)

                except ValueError:
                    print(" not good value for the row start")
                    csv_data = pd.read_csv(job.source_file.path,
                                           sep='\t',
                                           lineterminator='\r',
                                           skiprows=0,
                                           nrows=num_rows)
                print(csv_data)
            elif job.is_csv_source_file():
                try:
                    csv_data = pd.read_csv(job.source_file.path,
                                           skiprows=start_row_idx,
                                           nrows=num_rows)
                except ValueError:
                    print(" not good value for the row start")
                    csv_data = pd.read_csv(job.source_file.path,
                                           skiprows=0,
                                           nrows=num_rows)
                print(csv_data)
            else:
                return dict(success=False,
                            message='File type unknown (not csv or tab)')

            max_rows = len(csv_data)
            print("the no. of rows are ", max_rows)

            error_message = []
            if start_row > max_rows:
                err = ('The request was from %s rows but only %d'
                       ' rows were found, so default start rows = 1'
                       ' is set') % \
                       (start_row, max_rows)
                error_message.append(err)
                start_row = 1
                start_row_idx = start_row - 1
            if num_rows > max_rows:
                err = ('The request was for %s rows but only'
                       ' %d rows were found, so number rows'
                       ' is set to max rows') % \
                       (num_rows, max_rows)
                error_message.append(err)
                num_rows = max_rows

            print("error message", error_message)
            update_end_num = start_row + num_rows
            data_frame = csv_data[start_row_idx:update_end_num-1]
            response = HttpResponse(content_type='text/csv')

            csv_fname = 'data_rows_%s.csv' % (get_timestring_for_file())
            response['Content-Disposition'] = 'attachment; filename=%s' % csv_fname

            data_frame.to_csv(path_or_buf=response, sep=',', float_format='%.2f', index=False)

            return response

    @staticmethod
    def update_preprocess_metadata(preprocess_json, update_json, **kwargs):
        """To get the updated preprocess file from VariableDisplayUtil """

        var_util = VariableDisplayUtil(preprocess_json, update_json)
        if var_util.has_error:
            return False, var_util.get_error_messages()

        return True, var_util.get_updated_metadata()
