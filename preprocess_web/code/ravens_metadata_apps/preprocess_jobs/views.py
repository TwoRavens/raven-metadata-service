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
from col_info_constants import (UPDATE_VARIABLE_DISPLAY,UPDATE_CUSTOM_STATISTICS,DELETE_CUSTOM_STATISTICS,UPDATE_TO_CUSTOM_STATISTICS)
from np_json_encoder import NumpyJSONEncoder

def test_view(request):
    """test view"""
    return HttpResponse('hello')


def view_job_list(request):
    """Display a list of all jobs"""
    jobs = PreprocessJob.objects.all().order_by('-created')

    return render(request,
                  'preprocess/list.html',
                  {'jobs': jobs})


def view_job_detail(request,preprocess_id):
    """List the PreprocessJob and associated MetadataUpdates"""
    success, preprocess_list_or_err = JobUtil.get_versions_metadata_objects(preprocess_id)

    if not success:
        return JsonResponse(get_json_error(preprocess_list_or_err))

    for obj in preprocess_list_or_err:
        job_name = {'name': str(obj)}

    return render(request,
                  'preprocess/preprocess-job-detail.html',
                  {'iterable':True,
                   'jobs': preprocess_list_or_err,
                   'name': job_name,
                   'preprocess_id': preprocess_id})



def view_basic_upload_form(request):
    """Basic test form"""
    if request.method == 'POST':
        form = PreprocessJobForm(request.POST, request.FILES)
        if form.is_valid():
            job = form.save()

            JobUtil.start_preprocess(job)

            redirect_url = reverse('view_preprocess_job_status',
                                   kwargs=dict(job_id=job.id))

            return HttpResponseRedirect(redirect_url)
    else:
        form = PreprocessJobForm()

    return render(request,
                  'preprocess/view_basic_upload_form.html',
                  {'form': form})

@csrf_exempt
def view_custom_statistics_delete(request):
    """ to delete the custom_statistics"""
    """ expected input:
    {
   "preprocess_id":1,
   "custom_statistics":[
      {
         "id":"id_1",
         "delete":[
            "description",
            "replication"
         ]
      },
      {
         "id":"id_2",
         "delete":[
            "id"
         ]
        }
      ]
    }
    """
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
    job_id = update_json_or_err['preprocess_id']
    custom_statistics_json = update_json_or_err['custom_statistics']

    success, latest_metadata_json_or_err = JobUtil.get_latest_metadata(job_id)
    if success is False:
        user_msg = dict(success=False,
                        message=latest_metadata_json_or_err)
        return JsonResponse(user_msg)

    metadata_update_or_err = MetadataUpdateUtil(job_id, custom_statistics_json, \
                                               DELETE_CUSTOM_STATISTICS)
    if metadata_update_or_err.has_error:
        msg = get_json_error(metadata_update_or_err)
        user_msg = dict(success=False,
                        message='Custom Statistics',
                        id=job_id,
                        data=msg)

    else:
        user_msg = dict(success=True,
                        message='Custom Statistics',
                        id=job_id,
                        data=metadata_update_or_err.get_updated_metadata())
        print("Updated metadata : ", metadata_update_or_err)

    return JsonResponse(user_msg)


@csrf_exempt
def view_custom_statistics_update(request):
    """ the update for custom statistics"""
    """
            {
  "preprocess_id": 1,
  "custom_statistics": [
    {
      "id": "id_1",
      "updates": {
        "name": "Fourth order statistic",
        "value": 40
      }
    },
    {
      "updates": {
        "name": "This will be a new statistic",
        "value": 40
      }
    }
  ]
}
    """
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
    job_id = update_json_or_err['preprocess_id']
    custom_statistics_json = update_json_or_err['custom_statistics']

    success, latest_metadata_json_or_err = JobUtil.get_latest_metadata(job_id)
    if success is False:
        user_msg = dict(success=False,
                        message=latest_metadata_json_or_err)
        return JsonResponse(user_msg)

    metadata_update_or_err = MetadataUpdateUtil(job_id, custom_statistics_json, \
                                                UPDATE_TO_CUSTOM_STATISTICS)
    if metadata_update_or_err.has_error:
        msg = get_json_error(metadata_update_or_err)
        user_msg = dict(success=False,
                        message='Custom Statistics',
                        id=job_id,
                        data=msg)

    else:
        user_msg = dict(success=True,
                        message='Custom Statistics',
                        id=job_id,
                        data=metadata_update_or_err.get_updated_metadata())
        print("Updated metadata : ", metadata_update_or_err)

    return JsonResponse(user_msg)

@csrf_exempt
def view_custom_statistics_form(request):
    """ HTML form to get the custom statistics"""

    """
    expected input:
    {
   "preprocess_id":1677,
   "custom_statistics":[
      {
         "name":"Third order statistic",
         "variables":"lpop,bebop",
         "image":"http://www.google.com",
         "value":23.45,
         "description":"Third smallest value",
         "replication":"sorted(X)[2]",
         "viewable":false
      },
      {
         "name":"Fourth order statistic",
         "variables":"pop,bebop",
         "image":"http://www.youtube.com",
         "value":29.45,
         "description":"Fourth smallest value",
         "replication":"sorted(X)[3]",
         "viewable":false
      },
    {custom_statistics3}...
    ]
    }
    """
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
    job_id = update_json_or_err['preprocess_id']
    custom_statistics_json = []
    # form_data = json.loads(update_json_or_err)
    for data in update_json_or_err['custom_statistics']:
        frm = CustomStatisticsForm(data)

        if not frm.is_valid():
            user_msg = dict(success=False,
                            message='Invalid input',
                            errors=frm.errors)
            return JsonResponse(user_msg)

        custom_statistics_json.append(data)

    success, latest_metadata_json_or_err = JobUtil.get_latest_metadata(job_id)
    if success is False:
        user_msg = dict(success=False,
                        message=latest_metadata_json_or_err)
        return JsonResponse(user_msg)

    metadata_update_or_err = MetadataUpdateUtil(job_id, custom_statistics_json, \
                                                UPDATE_CUSTOM_STATISTICS)
    if metadata_update_or_err.has_error:
        msg = get_json_error(metadata_update_or_err)
        user_msg = dict(success=False,
                        message='Custom Statistics',
                        id=job_id,
                        data=msg)

    else:
        user_msg = dict(success=True,
                        message='Custom Statistics',
                        id=job_id,
                        data=metadata_update_or_err.get_updated_metadata())
        print("Updated metadata : ",metadata_update_or_err)

    return JsonResponse(user_msg)
    # ------------------------

def view_retrieve_rows_form(request):
    """HTML form to retrieve rows from a preprocess file"""
    if request.method != 'POST':
        frm = RetrieveRowsForm()
        return render(request,
                      'preprocess/retrieve-rows.html',
                      {'form': frm})

    frm = RetrieveRowsForm(request.POST)
    if not frm.is_valid():
        user_msg = dict(success=False,
                        message='Invalid input',
                        errors=frm.errors)

        return JsonResponse(user_msg)

    job_id = frm.cleaned_data['preprocess_id']

    job = JobUtil.get_completed_preprocess_job(job_id)
    if not job:
        raise Http404('job_id not found: %s' % job_id)

    input_format = frm.cleaned_data.get('format')
    if input_format == FORMAT_JSON:
        resp_info = JobUtil.retrieve_rows_json(job, **frm.cleaned_data)
        if not resp_info.success:
            return JsonResponse(get_json_error(resp_info.err_msg))

        return JsonResponse(resp_info.result_obj)

    elif input_format == FORMAT_CSV:
        csv_resp = JobUtil.retrieve_rows_csv(request, job, **frm.cleaned_data)
        return csv_resp

    # Shouldn't reach here, e.g. form should check
    err_msg = 'Unknown format: %s' % input_format
    return JsonResponse(get_json_error(err_msg))



def view_preprocess_job_status(request, job_id):
    """Show the state of an uploaded preprocess file"""
    try:
        job = PreprocessJob.objects.get(pk=job_id)
    except PreprocessJob.DoesNotExist:
        raise Http404('job_id not found: %s' % job_id)

    #check_job_status(job)

    info_dict = dict(job=job,
                     preprocess_string_err=False)

    if job.is_finished():
        data_ok, preprocess_string = job.get_metadata(as_string=True)
        if data_ok:
            info_dict['preprocess_string'] = preprocess_string
        else:
            info_dict['preprocess_string_err'] = True
    else:
        info_dict['current_time'] = get_current_timestring()

    return render(request,
                  'preprocess/view_preprocess_status.html',
                  info_dict)



"""
http://127.0.0.1:8080/preprocess/api-single-file

curl -H "Authorization: token 4db9ac8fd7f4465faf38a9765c8039a7" -X POST http://127.0.0.1:8080/preprocess/api-single-file

curl -H "Authorization: token 2e92d83e53e0436abd88e7c4688c49ea" -F source_file=@/Users/ramanprasad/Documents/github-rp/raven-metadata-service/test_data/fearonLaitin.csv http://127.0.0.1:8080/preprocess/api/process-single-file

curl -F "fieldNameHere=@myfile.html"  http://myapi.com/

curl -H "Content-Type: application/json" -X POST -d '{"username":"xyz","password":"xyz"}' http://localhost:3000/api/login

import requests
import os
from os.path import isfile, isdir, join
url = 'http://127.0.0.1:8000/preprocess/api-single-file'

sess = requests.Session()


fpath = '/Users/ramanprasad/Documents/github-rp/raven-metadata-service/test_data/fearonLaitin.csv'
files = {'source_file': open(fpath, 'rb')}
headers={'Authorization': 'token a919e9a542e24620be1a8a0830a8cbf7'}
r = sess.post(url, headers=headers, files=files)
r.text
open(join(os.getcwd(), 'err.html'), 'w').write(r.text)

"""

def show_job_info(request, job_id):
    """test to show uploaded file info"""
    try:
        job = PreprocessJob.objects.get(pk=job_id)
    except PreprocessJob.DoesNotExist:
        raise Http404('job_id not found: %s' % job_id)

    check_job_status(job)

    if 'pretty' in request.GET:
        jstring = json_dump(job.as_dict(), indent=4)
        return HttpResponse('<pre>%s</pre>' % jstring)

    user_msg = dict(success=True,
                    message='some message',
                    callback_url=job.get_job_status_link(),
                    data=job.as_dict())

    return JsonResponse(user_msg)
