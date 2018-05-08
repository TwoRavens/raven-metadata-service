"""Views for preprocess jobs"""
import json, collections
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from decimal import Decimal
from django.http import \
    (JsonResponse, HttpResponse,
     Http404, HttpResponseRedirect,
     QueryDict)
from django.contrib.auth.decorators import login_required
from django.core.files.base import ContentFile

from django.utils.decorators import method_decorator
from django.template.loader import render_to_string

from ravens_metadata_apps.utils.time_util import get_current_timestring
from ravens_metadata_apps.utils.metadata_file import get_metadata_filename
from ravens_metadata_apps.preprocess_jobs.decorators import apikey_required
from ravens_metadata_apps.raven_auth.models import User, KEY_API_USER
from ravens_metadata_apps.preprocess_jobs.job_util import JobUtil
from ravens_metadata_apps.preprocess_jobs.models import \
    (PreprocessJob, MetadataUpdate)
from ravens_metadata_apps.preprocess_jobs.forms import \
    (PreprocessJobForm, RetrieveRowsForm, CustomStatisticsForm,
     FORMAT_JSON, FORMAT_CSV)
from ravens_metadata_apps.utils.view_helper import \
    (get_request_body_as_json,
     get_json_error,
     get_json_success,
     get_baseurl_from_request)
from ravens_metadata_apps.preprocess_jobs.metadata_update_util import MetadataUpdateUtil
from ravens_metadata_apps.preprocess_jobs.tasks import check_job_status
from ravens_metadata_apps.utils.json_util import json_dump
from col_info_constants import UPDATE_VARIABLE_DISPLAY,UPDATE_CUSTOM_STATISTICS
from np_json_encoder import NumpyJSONEncoder


#@apikey_required
@csrf_exempt
def api_process_single_file(request, api_user=None):
    """Preprocess a single file
    - Always returns JSON
    - If not a POST:
        - return error
        - success:

    - General message format:
            { "success" : true/false,
              "message" : "e.g if error, put message here",
              "status" : finished/not finished
              "state" : what stage, e.g. preprocess started...
              "progress" : % completed
              "preprocess_status_url" : gives details of PreprocessInfo
             }
    """
    if not request.method == 'POST':
        err_msg = 'Must be a POST'
        return JsonResponse(get_json_error(err_msg),
                            status=412)

    # This duplicates the apikey_required decorator,
    # exists in case decorator is accidentally removed
    #
    #if not isinstance(api_user, User):
    #    return JsonResponse(get_json_error('Authorization failed.'),
    #                        status=401)

    form = PreprocessJobForm(request.POST, request.FILES)

    if not form.is_valid():
        user_msg = dict(success=False,
                        message='Errors found',
                        errors=form.errors.as_json())

        return JsonResponse(user_msg,
                            status=400)


    # save the PreprocessJob
    job = form.save()

    if api_user:
        job.creator = api_user
    job.save()

    # start background task
    JobUtil.start_preprocess(job)

    base_url = get_baseurl_from_request(request)

    user_msg = get_json_success(\
                'In progress',
                callback_url=job.get_job_status_link(base_url),
                data=job.as_dict())

    return JsonResponse(user_msg)


@csrf_exempt
def view_api_retrieve_rows(request):
    """API endpoint to retrieve rows from a preprocess file"""
    if request.method != 'POST':
        user_msg = 'Please use a POST to access this endpoint'
        return JsonResponse(get_json_error(user_msg))

    # Retrieve the JSON request from the body
    #
    success, update_json_or_err = get_request_body_as_json(request)
    if success is False:
        return JsonResponse(get_json_error(update_json_or_err))

    frm = RetrieveRowsForm(update_json_or_err)
    if not frm.is_valid():
        user_msg = dict(success=False,
                        message='Invalid input',
                        errors=frm.errors)
        return JsonResponse(user_msg)

    job_id = frm.cleaned_data['preprocess_id']

    job = JobUtil.get_completed_preprocess_job(job_id)

    input_format = frm.cleaned_data.get('format')

    if input_format == FORMAT_JSON:
        output = JobUtil.retrieve_rows_json(job, **frm.cleaned_data)
        #print("output ", output)
        user_msg = output
        return JsonResponse(user_msg)

    elif input_format == FORMAT_CSV:
        return JobUtil.retrieve_rows_csv(request, job, **frm.cleaned_data)

    user_msg = 'Unknown input_format: %s' % input_format
    return JsonResponse(get_json_error(user_msg))


@csrf_exempt
def api_update_metadata(request):
    """ API endpoint to get JSON request for updating the Preprocess metadata"""
    if request.method != 'POST':
        user_msg = 'Please use a POST to access this endpoint'
        return JsonResponse(get_json_error(user_msg))

    # Retrieve the JSON request from the body
    #
    success, update_json_or_err = get_request_body_as_json(request)
    if success is False:
        return JsonResponse(get_json_error(update_json_or_err))

    # Make sure there's a preprocess_id
    #
    update_json = update_json_or_err
    if 'preprocess_id' not in update_json:
        user_msg = 'preprocess_id not found: %s' % update_json['preprocess_id']
        return JsonResponse(get_json_error(user_msg))

    preprocess_id = update_json['preprocess_id']

    update_util = MetadataUpdateUtil(preprocess_id, update_json, UPDATE_VARIABLE_DISPLAY)
    if update_util.has_error:
        return JsonResponse(get_json_error(update_util))


    result = get_json_success('Success!',
                              data=update_util.get_updated_metadata())

    return JsonResponse(result)


def api_get_job_status_with_html(request, preprocess_id):
    """Return job status info with a chunk of HTML"""
    return api_get_job_status(request,
                              preprocess_id,
                              with_html=True)


def api_get_job_status(request, preprocess_id, with_html=False):
    """Return the PreprocessJob status, including data if available.
    Used to display the status of a PreprocessJob
    """
    try:
        job = PreprocessJob.objects.get(pk=preprocess_id)
    except PreprocessJob.DoesNotExist:
        err_mg = 'PreprocessJob not found for id: %d' % preprocess_id
        return JsonResponse(get_json_error(err_mg),
                            status=404)

    resp_info = job.as_dict()
    if with_html:
        status_row_html = render_to_string('preprocess/job_card_rows.html',
                                           dict(job=job))
        resp_info['status_row_html'] = status_row_html

    json_success = get_json_success('job retrieved',
                                    data=resp_info)
    if 'pretty' in request.GET:
        is_success, jstring = json_dump(json_success, indent=4)
        return HttpResponse('<pre>%s</pre>' % jstring)

    return JsonResponse(json_success)

    #json_fail = get_json_error(resp_info.err_msg)
    #if 'pretty' in request.GET:
    #    is_success, jstring = json_dump(json_fail, indent=4)
    #    return HttpResponse('<pre>%s</pre>' % jstring)

    #return JsonResponse(json_fail)


def api_get_latest_metadata(request, preprocess_id):
    """Return the latest version of the preprocess metadata"""

    success, metadata_or_err = JobUtil.get_latest_metadata(preprocess_id)

    if not success:
        return JsonResponse(get_json_error(metadata_or_err))


    user_msg = get_json_success(user_msg="Metadata retrieved",
                                data=metadata_or_err)

    if 'pretty' in request.GET:
        is_success, jstring = json_dump(user_msg, indent=4)
        return HttpResponse('<pre>%s</pre>' % jstring)

    return JsonResponse(user_msg)


def api_download_latest_metadata(request, preprocess_id):
    """Return the metadata JSON as an attachment"""

    success, metadata_or_err = JobUtil.get_latest_metadata(preprocess_id)
    if not success:
        return JsonResponse(get_json_error(metadata_or_err))

    # Prepare the response
    #
    response = HttpResponse(content_type='json')

    # (no check against int b/c retrieval already worked)
    fname = get_metadata_filename(preprocess_id)

    response['Content-Disposition'] = 'attachment; filename=%s' % fname

    json.dump(metadata_or_err,
              fp=response,
              indent=4,
              cls=NumpyJSONEncoder)

    return response



def api_download_version(request, preprocess_id, version):
    """Download preprocess info by version"""

    if version:
        # use this param for the query
        version_decimal = Decimal(str(version))
    else:
        # Default to version 1.0
        version_decimal = Decimal('1.0')

    # Return the latest version of the preprocess metadata
    #
    success, metadata_obj_or_err = JobUtil.get_version_metadata_object(\
                                    preprocess_id, version_decimal)
    if not success:
        return JsonResponse(get_json_error(metadata_obj_or_err))

    fname = get_metadata_filename(preprocess_id,
                                    metadata_obj_or_err.get_version_string())

    response = HttpResponse(content_type='json')
    response['Content-Disposition'] = 'attachment; filename=%s' % fname

    metadata_found, metadata_or_err = metadata_obj_or_err.get_metadata()
    if not metadata_found:
        return JsonResponse(get_json_error(metadata_or_err))

    json.dump(metadata_or_err,
              fp=response,
              indent=4,
              cls=NumpyJSONEncoder)
    return response



def api_get_metadata_version(request, preprocess_id, version):
    """Return a specific version of the preprocess metadata"""
    version_decimal = Decimal(str(version))
    success, metadata_or_err = JobUtil.get_version_metadata_object(\
                        preprocess_id, version_decimal)

    if not success:
        return JsonResponse(get_json_error(metadata_or_err))


    success, data_or_err = metadata_or_err.get_metadata()
    if not success:
        return JsonResponse(get_json_error(data_or_err))

    if 'pretty' in request.GET:
        is_success, jstring = json_dump(data_or_err, indent=4)
        return HttpResponse('<pre>%s</pre>' % jstring)


    return JsonResponse(get_json_success('Success', data=data_or_err))
