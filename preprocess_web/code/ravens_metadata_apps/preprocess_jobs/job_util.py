"""Utility class for the preprocess workflow"""
"""Utility class for the preprocess workflow"""
import pandas as pd
from django.http import HttpResponse, JsonResponse

import col_info_constants as col_const
import update_constants as update_const
from preprocess_runner import KEY_JSONLD_CITATION
from ravens_metadata_apps.preprocess_jobs.tasks import \
    (preprocess_csv_file,)
from ravens_metadata_apps.utils.time_util import get_timestring_for_file
from ravens_metadata_apps.utils.basic_response import \
    (ok_resp, err_resp)
from ravens_metadata_apps.preprocess_jobs.models import \
    (PreprocessJob, MetadataUpdate)
from variable_display_util import VariableDisplayUtil
from ravens_metadata_apps.utils.json_util import remove_nan_from_dict
from file_format_constants import TAB_FILE_EXT
from ravens_metadata_apps.utils.view_helper import get_json_error
from custom_statistics_util import CustomStatisticsUtil
from ravens_metadata_apps.utils.view_helper import get_json_error


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

        #print('type(obj_or_err)', type(obj_or_err))
        #print('obj_or_err.id', obj_or_err.id)
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
                                  version_number=version\
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

        # update the state of the job
        job.set_state_pending()
        job.save()

        # Additional/optional arguments for preprocess
        #
        additional_args = dict(job_id=job.id)
        dv_file_info = job.dataversefileinfo_set.first()
        if dv_file_info and dv_file_info.jsonld_citation:
            additional_args[KEY_JSONLD_CITATION] = dv_file_info.jsonld_citation
        # send the file to the queue
        #
        task = preprocess_csv_file.delay(\
                    job.source_file.path,
                    **additional_args)

        # set the task_id
        job.task_id = task.id

        # save the new state
        job.save()

    @staticmethod
    def get_data_frame(job, **kwargs):
        """Return a dataframe"""

        start_row = kwargs.get('start_row')
        num_rows = kwargs.get('num_rows')
        #change_nas_to_null = kwargs.get('change_nas_to_null', True)

        # ------------------------------------------
        # Check the errors
        # ------------------------------------------
        error_message = []
        job_data = job.get_metadata()
        if not job_data.success:
            return False, None, job_data.err_msg

        job_metadata = job_data.result_obj  # in this case job_data is an `ok_resp`
        row_cnt = job_metadata[col_const.DATASET_LEVEL_KEY][col_const.DATASET_ROW_CNT]

        if start_row > row_cnt:
            err_msg = 'The start row, %s, exceeds the total number of rows, %d.' \
                        % (start_row, row_cnt)
            return False, None, err_msg

        if start_row == 1 and num_rows > row_cnt:
            err_msg = 'Note: The request was for %s row(s) but only %d rows were found.' \
                  % (num_rows, row_cnt)
            error_message.append(err_msg)
            num_rows = row_cnt

        elif (start_row + num_rows) > row_cnt:
            num_rows_avail = row_cnt - start_row
            err_msg = ('Note: The request was for %s row(s) starting'
                       ' at row %d.') % \
                       (num_rows, start_row)

            # Case where no rows are available
            #
            if num_rows_avail < 1:
                err_msg = ('%s However, no rows are available'
                           ' when starting with row %d. (total rows: %s)') % \
                           (err_msg, start_row, row_cnt)
                return False, None, err_msg

            err_msg = ('%s However, only %d row(s) were found'
                       ' starting with row %d') % \
                       (err_msg, num_rows_avail, start_row)

            error_message.append(err_msg)
            num_rows = num_rows_avail

        # To read csv given rows count and start rows
        if job.is_tab_source_file():

            try:
                csv_data = pd.read_csv(job.source_file.path,
                                       sep='\t',
                                       #lineterminator='\r',
                                       skiprows=range(1, start_row),
                                       # skip rows range starts from 1 as 0 row is the header
                                       nrows=num_rows)

            except ValueError:
                print(" not good value for the row start")
                start_row = 1
                csv_data = pd.read_csv(job.source_file.path,
                                       sep='\t',
                                       lineterminator='\r',
                                       skiprows=range(1, start_row),
                                       # skip rows range starts from 1 as 0 row is the header
                                       nrows=num_rows)
        elif job.is_csv_source_file():
            try:
                csv_data = pd.read_csv(job.source_file.path,
                                       skiprows=range(1, start_row),
                                       # skip rows range starts from 1 as 0 row is the header
                                       nrows=num_rows)
            except ValueError:
                print(" not good value for the row start")
                start_row = 1
                csv_data = pd.read_csv(job.source_file.path,
                                       skiprows=range(1, start_row),
                                       # skip rows range starts from 1 as 0 row is the header
                                       nrows=num_rows)
        else:
            return err_resp('File type unknown (not csv or tab)')

        return True, csv_data, error_message

    @staticmethod
    def retrieve_rows_json(job, **kwargs):
        """Open the original data file and return the rows in JSON format (python dict)"""
        start_row = kwargs.get(update_const.START_ROW)
        num_rows = kwargs.get(update_const.NUM_ROWS)
        input_format = kwargs.get('format')
        job_id = kwargs.get(col_const.PREPROCESS_ID)

        # Retrieve the dataframe
        #
        success, data_frame, error_message = JobUtil.get_data_frame(\
                                            job,
                                            start_row=start_row,
                                            num_rows=num_rows)
        if not success:
            return err_resp(error_message)

        raw_data = data_frame.to_dict(orient='split')

        info_result = remove_nan_from_dict(raw_data)
        if not info_result.success:
            return err_resp(info_result.err_msg)

        formatted_json_data = info_result.result_obj

        # Remove the index
        #
        if 'index' in formatted_json_data:
            del formatted_json_data['index']

        if len(error_message) > 0:
            output = {
                "success": True,
                "message": 'It worked but with some changes',
                "modifications": error_message,
                "attributes": {
                    col_const.PREPROCESS_ID: job_id,
                    update_const.START_ROW: start_row,
                    update_const.NUM_ROWS: num_rows,
                    "format": input_format
                },
                "data": formatted_json_data,
            }

        else:
            output = {
                "success": True,
                "message": 'It worked',
                "attributes": {
                    col_const.PREPROCESS_ID: job_id,
                    update_const.START_ROW: start_row,
                    update_const.NUM_ROWS: num_rows,
                    "format": input_format
                },
                "data": formatted_json_data,
            }

        return ok_resp(output)

    @staticmethod
    def retrieve_rows_csv(request, job, **kwargs):
        """Return data rows as a .csv file."""
        if request.method == 'POST':
            start_row = kwargs.get(update_const.START_ROW)
            num_rows = kwargs.get(update_const.NUM_ROWS)
            success, data_frame, err_resp = JobUtil.get_data_frame(\
                                                job,
                                                start_row=start_row,
                                                num_rows=num_rows)
            if success:
                response = HttpResponse(content_type='text/csv')

                csv_fname = 'data_rows_%s.csv' % (get_timestring_for_file())
                response['Content-Disposition'] = 'attachment; filename=%s' % csv_fname

                data_frame.to_csv(path_or_buf=response, sep=',', float_format='%.2f', index=False)

                return response
            else:
                return JsonResponse(get_json_error(err_resp))

    @staticmethod
    def update_preprocess_metadata(preprocess_json, update_json, **kwargs):
        """To get the updated preprocess file from VariableDisplayUtil """

        var_util = VariableDisplayUtil(preprocess_json, update_json)
        if var_util.has_error:
            return False, var_util.get_error_messages()

        return True, var_util.get_updated_metadata()

    @staticmethod
    def update_preprocess_metadata_custom_statistics(job_id,custom_statistics_json):
        """ Send info to the custom_statistics in preprocess runner"""
        success,latest_metadata_json_or_err = JobUtil.get_latest_metadata(job_id)
        if success is False:
            user_msg = dict(success=False,
                            message=latest_metadata_json_or_err)
            return user_msg

        custom_util = CustomStatisticsUtil(latest_metadata_json_or_err, custom_statistics_json)
        custom_util.custom_statistics_update()
        if custom_util.has_error:
            return False, custom_util.get_error_messages()

        return True, custom_util.get_updated_metadata()

    @staticmethod
    def update_custom_statistics(job_id, version, update_json):
        """ send the updates list in the json to custom statistics"""

        success, version_metadata_json_or_err = JobUtil.get_version_metadata_object(job_id,version)
        if success is False:
            user_msg = dict(success=False,
                            message=version_metadata_json_or_err)
            return user_msg
        success, data_or_err = version_metadata_json_or_err.get_metadata()
        if not success:
            return JsonResponse(get_json_error(data_or_err))

        # print(" version object ", data_or_err)
        custom_util_update = CustomStatisticsUtil(data_or_err, update_json)
        custom_util_update.update_custom_stats()
        print("updated custom _ stats", custom_util_update.get_updated_metadata())
        if custom_util_update.has_error:
            return False, custom_util_update.get_error_messages()

        return True, custom_util_update.get_updated_metadata()
