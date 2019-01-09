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
