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

from ravens_metadata_apps.utils.metadata_file import get_preprocess_filename
from ravens_metadata_apps.preprocess_jobs.decorators import apikey_required
from ravens_metadata_apps.raven_auth.models import User, KEY_API_USER
from ravens_metadata_apps.preprocess_jobs.job_util import JobUtil
from ravens_metadata_apps.preprocess_jobs.models import \
    (PreprocessJob, MetadataUpdate)
from ravens_metadata_apps.preprocess_jobs.forms import \
    (PreprocessJobForm, RetrieveRowsForm,
     FORMAT_JSON, FORMAT_CSV)
from ravens_metadata_apps.utils.view_helper import \
    (get_request_body_as_json,
     get_json_error,
     get_json_success,
     get_baseurl_from_request)
from ravens_metadata_apps.preprocess_jobs.metadata_update_util import MetadataUpdateUtil
from np_json_encoder import NumpyJSONEncoder

# Create your views here.
def test_view(request):
    from ravens_metadata.celery import debug_task
    debug_task.delay()
    return HttpResponse('hello')


def view_job_list(request):
    """Display a list of all jobs"""
    jobs = PreprocessJob.objects.all().order_by('-created')

    return render(request,
                  'preprocess/list.html',
                  {'jobs': jobs})


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

    fname = get_preprocess_filename(preprocess_id,
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




def api_download_latest_metadata(request, preprocess_id):
    """Return the metadata JSON as an attachment"""

    success, metadata_or_err = JobUtil.get_latest_metadata(preprocess_id)
    if not success:
        return JsonResponse(get_json_error(metadata_or_err))

    # Prepare the response
    #
    response = HttpResponse(content_type='json')

    # (no check against int b/c retrieval already worked)
    fname = get_preprocess_filename(preprocess_id)

    response['Content-Disposition'] = 'attachment; filename=%s' % fname

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
        jstring = json.dumps(data_or_err, indent=4, cls=NumpyJSONEncoder)
        return HttpResponse('<pre>%s</pre>' % jstring)


    return JsonResponse(get_json_success('Success', data=data_or_err))


def api_detail(request,preprocess_id):
    """ get all the versions and detail of the preprocess job"""
    print("job_id", preprocess_id)
    """Return the latest version of the preprocess metadata"""

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
        #print("output ", output)
        user_msg = output
        return JsonResponse(user_msg)
    elif input_format == FORMAT_CSV:
        return JobUtil.retrieve_rows_csv(request, job, **frm.cleaned_data)



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

    try:
        job = PreprocessJob.objects.get(pk=job_id)
    except PreprocessJob.DoesNotExist:
        raise Http404('job_id not found: %s' % job_id)

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

    update_util = MetadataUpdateUtil(preprocess_id, update_json)
    if update_util.has_error:
        return JsonResponse(get_json_error(update_util.error_messages))


    result = get_json_success('Success!',
                              data=update_util.get_updated_metadata())

    return JsonResponse(result)



def api_get_latest_metadata(request, preprocess_id):
    """Return the latest version of the preprocess metadata"""

    success, metadata_or_err = JobUtil.get_latest_metadata(preprocess_id)

    if not success:
        return JsonResponse(get_json_error(metadata_or_err))


    user_msg = get_json_success(user_msg="Metadata retrieved",
                                data=metadata_or_err)

    if 'pretty' in request.GET:
        jstring = json.dumps(user_msg, indent=4, cls=NumpyJSONEncoder)
        return HttpResponse('<pre>%s</pre>' % jstring)

    return JsonResponse(user_msg)




def view_job_status_page(request, job_id):
    """test to show uploaded file info"""
    try:
        job = PreprocessJob.objects.get(pk=job_id)
    except PreprocessJob.DoesNotExist:
        raise Http404('job_id not found: %s' % job_id)

    JobUtil.check_status(job)

    info_dict = dict(job=job,
                     preprocess_string_err=False)

    if job.is_finished():
        data_ok, preprocess_string = job.get_metadata(as_string=True)
        if data_ok:
            info_dict['preprocess_string'] = preprocess_string
        else:
            info_dict['preprocess_string_err'] = True

    return render(request,
                  'preprocess/view_process_status.html',
                  info_dict)



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
        jstring = json.dumps(job.as_dict(), indent=4, cls=NumpyJSONEncoder)
        return HttpResponse('<pre>%s</pre>' % jstring)

    user_msg = dict(success=True,
                    message='some message',
                    callback_url=job.get_job_status_link(),
                    data=job.as_dict())

    return JsonResponse(user_msg)
