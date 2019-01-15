import json, collections
from decimal import Decimal

from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.http import \
    (JsonResponse, HttpResponse,
     Http404, HttpResponseRedirect)

from django.contrib.auth.decorators import login_required
from ravens_metadata_apps.preprocess_jobs.forms import \
    (PreprocessJobForm, FORMAT_JSON, FORMAT_CSV)

from ravens_metadata_apps.r_preprocess.preprocess_util import PreprocessUtil
from ravens_metadata_apps.r_preprocess.tasks import run_r_preprocess_file

from ravens_metadata_apps.utils.view_helper import \
    (get_request_body_as_json,
     get_json_error,
     get_json_success,
     get_baseurl_from_request)

@csrf_exempt
def view_r_preprocess_form_direct(request):
    """Not for prod: Basic test form to run preprocess.R directly"""
    if request.method == 'POST':
        form = PreprocessJobForm(request.POST, request.FILES)
        if form.is_valid():
            job = form.save()

            putil = PreprocessUtil(job.id)
            if putil.has_error():
                return HttpResponse(putil.get_error_message())

            redirect_url = reverse('view_job_versions',
                                   kwargs=dict(preprocess_id=job.id))
            return HttpResponseRedirect(redirect_url)
    else:
        form = PreprocessJobForm()

    info_dict = dict(form=form,
                     NO_QUEUE=True)

    return render(request,
                  'r_preprocess/view_r_preprocess_form.html',
                  info_dict)


@csrf_exempt
def view_r_preprocess_form(request):
    """Basic test form to run preprocess.R via celery queue"""
    if request.method == 'POST':
        form = PreprocessJobForm(request.POST, request.FILES)
        if form.is_valid():
            job = form.save()

            run_r_preprocess_file.delay(job.id)
            #putil = PreprocessUtil(job.id)
            #if putil.has_error():
            #    return HttpResponse(putil.get_error_message())
            #else:
            #    redirect_url = reverse('view_job_versions',
            #                           kwargs=dict(preprocess_id=job.id))
            redirect_url = reverse('view_preprocess_job_status',
                                   kwargs=dict(job_id=job.id))
            return HttpResponseRedirect(redirect_url)
    else:
        form = PreprocessJobForm()

    return render(request,
                  'r_preprocess/view_r_preprocess_form.html',
                  {'form': form})

@csrf_exempt
def api_r_preprocess_form(request):
    """Basic test form to run preprocess.R via celery queue"""
    if not request.method == 'POST':
        err_msg = ('Please send a POST request to process a file.'
                   ' Example: ')
        return JsonResponse(get_json_error(err_msg),
                            status=412)

    form = PreprocessJobForm(request.POST, request.FILES)
    if not form.is_valid():
        user_msg = dict(success=False,
                        message='Errors found',
                        errors=form.errors.as_json())
        return JsonResponse(user_msg,
                            status=400)

    job = form.save()

    run_r_preprocess_file.delay(job.id)

    base_url = get_baseurl_from_request(request)

    user_msg = get_json_success(\
                'In progress',
                callback_url=job.get_job_status_link(base_url),
                data=job.as_dict())

    return JsonResponse(user_msg)
