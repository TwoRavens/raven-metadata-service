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
from django.conf import settings

import col_info_constants as col_const
import update_constants as update_const

from ravens_metadata_apps.utils.time_util import get_current_timestring
from ravens_metadata_apps.utils.metadata_file import get_metadata_filename
from ravens_metadata_apps.preprocess_jobs.decorators import apikey_required
from ravens_metadata_apps.raven_auth.models import User, KEY_API_USER
from ravens_metadata_apps.preprocess_jobs.job_util import JobUtil
from ravens_metadata_apps.preprocess_jobs.models import \
    (PreprocessJob, MetadataUpdate)
from ravens_metadata_apps.preprocess_jobs.forms import \
    (PreprocessJobForm, RetrieveRowsForm, CustomStatisticsForm,
     FORMAT_JSON, FORMAT_CSV,
     DEFAULT_START_ROW, DEFAULT_NUM_ROWS)
from ravens_metadata_apps.utils.view_helper import \
    (get_request_body_as_json,
     get_json_error,
     get_json_success,
     get_baseurl_from_request,
     KEY_EDITOR_URL,
     HIDE_VERSIONS_BUTTON, HIDE_EDITOR_BUTTON)
from ravens_metadata_apps.preprocess_jobs.metadata_update_util import MetadataUpdateUtil
from ravens_metadata_apps.preprocess_jobs.tasks import check_job_status
from ravens_metadata_apps.utils.json_util import json_dump
from ravens_metadata_apps.dataverse_connect.models import DataverseFileInfo


def test_view(request):
    """test view"""



    return HttpResponse('hello')


def view_job_list(request):
    """Display a list of all jobs"""
    dv_lookup = {}
    for dv_info in DataverseFileInfo.objects.select_related('preprocess_job').all():
        dv_lookup[dv_info.preprocess_job.id] = dv_info

    jobs = PreprocessJob.objects.all().order_by('-created')
    job_list = []
    for job in jobs:
        job.dv_info = dv_lookup.get(job.id, None)
        job_list.append(job)

    info_dict = {'jobs': job_list,
                 KEY_EDITOR_URL: settings.EDITOR_URL}

    return render(request,
                  'preprocess/list.html',
                  info_dict)


def view_job_versions(request, preprocess_id):
    """List the PreprocessJob and associated MetadataUpdates"""
    success, preprocess_list_or_err = JobUtil.get_versions_metadata_objects(preprocess_id)

    if not success:
        return JsonResponse(get_json_error(preprocess_list_or_err))

    preprocess_job = JobUtil.get_completed_preprocess_job(preprocess_id)

    dv_info = DataverseFileInfo.objects.filter(\
                                preprocess_job=preprocess_job\
                                ).first()

    info_dict = {'iterable':True,
                 KEY_EDITOR_URL: settings.EDITOR_URL,
                 HIDE_VERSIONS_BUTTON: True,
                 'dv_info': dv_info,
                 'jobs': preprocess_list_or_err,
                 'preprocess_job': preprocess_job,
                 'name': preprocess_job.name,
                 col_const.PREPROCESS_ID: preprocess_id}

    return render(request,
                  'preprocess/preprocess-job-detail.html',
                  info_dict)


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
    job_id = update_json_or_err[col_const.PREPROCESS_ID]
    custom_statistics_json = update_json_or_err[col_const.CUSTOM_KEY]

    success, latest_metadata_json_or_err = JobUtil.get_latest_metadata(job_id)
    if success is False:
        user_msg = dict(success=False,
                        message=latest_metadata_json_or_err)
        return JsonResponse(user_msg)

    metadata_update_or_err = MetadataUpdateUtil(\
                                job_id,
                                custom_statistics_json,
                                col_const.DELETE_CUSTOM_STATISTICS)
    if metadata_update_or_err.has_error:
        msg = metadata_update_or_err.get_error_messages()
        user_msg = dict(success=False,
                        message='Custom Statistics',
                        id=job_id,
                        data=msg)

    else:
        user_msg = dict(success=True,
                        message='Custom Statistics',
                        id=job_id,
                        data=metadata_update_or_err.get_updated_metadata())
        # print("Updated metadata : ", metadata_update_or_err)
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
    job_id = update_json_or_err[col_const.PREPROCESS_ID]
    custom_statistics_json = update_json_or_err[col_const.CUSTOM_KEY]

    success, latest_metadata_json_or_err = JobUtil.get_latest_metadata(job_id)
    if success is False:
        user_msg = dict(success=False,
                        message=latest_metadata_json_or_err)
        return JsonResponse(user_msg)

    metadata_update_or_err = MetadataUpdateUtil(\
                                        job_id,
                                        custom_statistics_json,
                                        col_const.UPDATE_TO_CUSTOM_STATISTICS)
    if metadata_update_or_err.has_error:
        msg = metadata_update_or_err.get_error_messages()
        user_msg = dict(success=False,
                        message='Custom Statistics',
                        id=job_id,
                        data=msg)

    else:
        user_msg = dict(success=True,
                        message='Custom Statistics',
                        id=job_id,
                        data=metadata_update_or_err.get_updated_metadata())
        # print("Updated metadata : ", metadata_update_or_err)

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
    job_id = update_json_or_err[col_const.PREPROCESS_ID]
    if job_id is None:
        return JsonResponse('%s is required' % col_const.PREPROCESS_ID)
    custom_statistics_json = []
    for data in update_json_or_err[col_const.CUSTOM_KEY]:
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

    metadata_update_or_err = MetadataUpdateUtil(job_id, custom_statistics_json,
                                                col_const.UPDATE_CUSTOM_STATISTICS)
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
        # print("Updated metadata : ", metadata_update_or_err)

    return JsonResponse(user_msg)
    # ------------------------


def view_retrieve_rows_form(request):
    """HTML form to retrieve rows from a preprocess file"""
    if request.method != 'POST':
        # Is there a default preprocess id in the url query string
        #
        if col_const.PREPROCESS_ID in request.GET:
            init_vals = {update_const.START_ROW: DEFAULT_START_ROW,
                         update_const.NUM_ROWS: DEFAULT_NUM_ROWS,
                         col_const.PREPROCESS_ID: request.GET[col_const.PREPROCESS_ID]}
            frm = RetrieveRowsForm(init_vals)
        else:
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

    job_id = frm.cleaned_data[col_const.PREPROCESS_ID]

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

    dv_info = DataverseFileInfo.objects.filter(\
                            preprocess_job=job\
                            ).first()

    info_dict = {'job': job,
                 'dv_info': dv_info,
                 KEY_EDITOR_URL: settings.EDITOR_URL,
                 #HIDE_VERSIONS_BUTTON: True,
                 'preprocess_string_err': False}

    # print('info_dict', info_dict)

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

curl -H "Authorization: token 2e92d83e53e0436abd88e7c4688c49ea" -F source_file=@/Users/ramanprasad/Documents/
github-rp/raven-metadata-service/test_data/fearonLaitin.csv http://127.0.0.1:8080/preprocess/api/process-single-file

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
        if jstring.success:
            return HttpResponse('<pre>%s</pre>' % jstring.result_obj)
        return JsonResponse(get_json_error(jstring.err_mg))

    user_msg = dict(success=True,
                    message='some message',
                    callback_url=job.get_job_status_link(),
                    data=job.as_dict())

    return JsonResponse(user_msg)


@csrf_exempt
def add_problems_section(request):
    """Add the problems section to the preprocess metadata"""
    """
    Sample:{
   "preprocessId":24,
   "version":1,
   "problems":[
      {
         "description":{"problem_id":"problem1","system":"auto","meaningful":"no","target":"Hits","predictors":
         ["At_bats","Runs","Doubles"],"transform":0,"subsetObs":0,"subsetFeats":0,"task":"regression","rating":3,
         "description":"Hits is predicted by At_bats and Runs and Doubles","metric":"meanSquaredError"},
         "results":{}
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
    job_id = update_json_or_err[col_const.PREPROCESS_ID]
    version = update_json_or_err[col_const.VERSION_KEY]
    if job_id is None:
        return JsonResponse('%s is required' % col_const.PREPROCESS_ID)

    success, latest_metadata_json_or_err = JobUtil.update_preprocess_problem_section(job_id, version, update_json_or_err)
    if success is False:
        user_msg = dict(success=False,
                        message=latest_metadata_json_or_err)
        return JsonResponse(user_msg)

    return JsonResponse(latest_metadata_json_or_err)






