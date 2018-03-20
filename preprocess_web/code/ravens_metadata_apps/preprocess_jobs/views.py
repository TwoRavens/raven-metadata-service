import json
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from django.http import JsonResponse, HttpResponse, Http404, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from ravens_metadata_apps.preprocess_jobs.job_util import JobUtil

from ravens_metadata_apps.preprocess_jobs.models import PreprocessJob
from ravens_metadata_apps.preprocess_jobs.forms import PreprocessJobForm

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
def endpoint_api_single_file(request):
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
    if request.method != 'POST':
        user_msg = dict(success=False,
                        message='Please use a POST request')
        return JsonResponse(user_msg,
                            status=412)

    form = PreprocessJobForm(request.POST, request.FILES)
    if not form.is_valid():

        user_msg = dict(success=False,
                        message='Errors found',
                        errors=form.errors.as_json())
        return JsonResponse(user_msg,
                            status=400)


    # save the PreprocessJob
    job = form.save()

    # start background task
    JobUtil.start_preprocess(job)

    user_msg = dict(success=True,
                    message='some message',
                    callback_url=job.get_job_status_link(),
                    data=job.as_dict())

    return JsonResponse(user_msg)

"""
import requests
import os
from os.path import isfile, isdir, join
url = 'http://127.0.0.1:8000/preprocess/api-single-file'


fpath = '/Users/ramanprasad/Documents/github-rp/raven-metadata-service/preprocess_web/test_setup_local/preprocess_files/source_file/2018/03/19/fearonLaitin.tab'
files = {'source_file': open(fpath, 'rb')}
r = requests.post(url, files=files)
r.text
open('err.html', 'w').write(r.text)

test_file_dir = '/Users/ramanprasad/Documents/github-rp/raven-metadata-service/preprocess/input/'

for fname in os.listdir(test_file_dir):
    if fname.endswith('.csv'):
        fullname = join(test_file_dir, fname)
        files = {'source_file': open(fullname, 'rb')}
        r = requests.post(url, files=files)
        r.text
        break

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


    #return JsonResponse(job.as_dict())
    #return render(request,
    #              'preprocess/view_process_status.html',
    #              {'job': job.as_dict()})
