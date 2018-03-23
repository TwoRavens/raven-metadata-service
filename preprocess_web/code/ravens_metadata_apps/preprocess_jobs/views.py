import json
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from django.http import JsonResponse, HttpResponse, Http404, HttpResponseRedirect
from django.contrib.auth.decorators import login_required

from django.utils.decorators import method_decorator

from ravens_metadata_apps.preprocess_jobs.job_util import JobUtil

from ravens_metadata_apps.raven_auth.models import User, KEY_API_USER
from ravens_metadata_apps.preprocess_jobs.job_util import JobUtil
from ravens_metadata_apps.preprocess_jobs.models import PreprocessJob
from ravens_metadata_apps.preprocess_jobs.forms import \
    (PreprocessJobForm, RetrieveRowsForm,
     FORMAT_JSON, FORMAT_CSV)
from ravens_metadata_apps.utils.view_helper import \
    (get_request_body_as_json,
     get_json_error,
     get_json_success,
     get_baseurl_from_request)


# Create your views here.
def test_view(request):
    from ravens_metadata.celery import debug_task
    debug_task.delay()
    return HttpResponse('hello')


def view_basic_upload_form(request):
    """Basic test form"""
    if request.method == 'POST':
        form = PreprocessJobForm(request.POST, request.FILES)
        if form.is_valid():
            job = form.save()

            JobUtil.start_preprocess(job)

            redirect_url = reverse('view_job_status_page',
                                   kwargs=dict(job_id=job.id))

            return HttpResponseRedirect(redirect_url)
    else:
        form = PreprocessJobForm()

    return render(request,
                  'preprocess/view_basic_upload_form.html',
                  {'form': form})

"""
def get_retrieve_rows_info(request, job_id):
    # if request == 'POST':
    try:
        job = PreprocessJob.objects.get(pk=job_id)
    except PreprocessJob.DoesNotExist:
        raise Http404('job_id not found: %s' % job_id)
    output = JobUtil.retrieve_rows(job)
    print("output ", output)
    return render(request,
                  'preprocess/retrieve-rows.html',
                  {'output': output})
"""

def view_retrieve_rows_form(request):
    """HTML form to retrieve rows from a preprocess file"""
    if request.method != 'POST':
        frm = RetrieveRowsForm()
        return render(request,
                      'preprocess/retrieve-rows.html',
                      {'form': frm})
    else:
        frm = RetrieveRowsForm(request.POST)
        if not frm.is_valid():
            user_msg = dict(success=False,
                            message='Invalid input',
                            errors=frm._errors)
            return JsonResponse(user_msg)

        try:
            job = PreprocessJob.objects.get(pk=frm.cleaned_data['preprocess_id'])
        except PreprocessJob.DoesNotExist:
            raise Http404('job_id not found: %s' % job_id)

        input_format = frm.cleaned_data.get('format')
        if input_format == FORMAT_JSON:
            output = JobUtil.retrieve_rows_json(job, **frm.cleaned_data)
            print("output ", output)
            user_msg = output
            return JsonResponse(user_msg)
        elif input_format == FORMAT_CSV:
            return JobUtil.retrieve_rows_csv(request, job, **frm.cleaned_data)



@csrf_exempt
def view_api_retrieve_rows(request):
    """API endpoint to retrieve rows from a preprocess file"""
    if request.method != 'POST':
        user_msg = dict(success=False,
                        message='Please use a POST to access this endpoint')
        return JsonResponse(user_msg)

    frm = RetrieveRowsForm(request.POST)
    if not frm.is_valid():
        user_msg = dict(success=False,
                        message='Invalid input',
                        errors=frm._errors)
        return JsonResponse(user_msg)

    try:
        job = PreprocessJob.objects.get(pk=frm.cleaned_data['preprocess_id'])
    except PreprocessJob.DoesNotExist:
        raise Http404('job_id not found: %s' % job_id)

    input_format = frm.cleaned_data.get('format')
    if input_format == FORMAT_JSON:
        output = JobUtil.retrieve_rows_json(job, **frm.cleaned_data)
        print("output ", output)
        user_msg = output
        return JsonResponse(user_msg)
    elif input_format == FORMAT_CSV:
        return JobUtil.retrieve_rows_csv(request, job, **frm.cleaned_data)


def view_job_status_page(request, job_id):
    """test to show uploaded file info"""
    try:
        job = PreprocessJob.objects.get(pk=job_id)
    except PreprocessJob.DoesNotExist:
        raise Http404('job_id not found: %s' % job_id)

    JobUtil.check_status(job)

    return render(request,
                  'preprocess/view_process_status.html',
                  {'job': job})



from ravens_metadata_apps.preprocess_jobs.decorators import apikey_required
@csrf_exempt
@apikey_required
def endpoint_api_single_file(request, api_user=None):
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
    if not isinstance(api_user, User):
        return JsonResponse(get_json_error('Authorization failed.'),
                            status=401)

    form = PreprocessJobForm(request.POST, request.FILES)

    if not form.is_valid():
        user_msg = dict(success=False,
                        message='Errors found',
                        errors=form.errors.as_json())

        return JsonResponse(user_msg,
                            status=400)


    # save the PreprocessJob
    job = form.save()

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

"""
http://127.0.0.1:8080/preprocess/api-single-file

curl -H "Authorization: token 4db9ac8fd7f4465faf38a9765c8039a7" -X POST http://127.0.0.1:8080/preprocess/api-single-file

curl -H "Authorization: token 2e92d83e53e0436abd88e7c4688c49ea" -F source_file=@/Users/ramanprasad/Documents/github-rp/raven-metadata-service/test_data/fearonLaitin.csv http://127.0.0.1:8080/preprocess/api-single-file

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

    JobUtil.check_status(job)

    if 'pretty' in request.GET:
        jstring = json.dumps(job.as_dict(), indent=4)
        return HttpResponse('<pre>%s</pre>' % jstring)

    user_msg = dict(success=True,
                    message='some message',
                    callback_url=job.get_job_status_link(),
                    data=job.as_dict())

    return JsonResponse(user_msg)
