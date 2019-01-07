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
from ravens_metadata_apps.preprocess_jobs.forms import \
    (PreprocessJobForm, RetrieveRowsForm, CustomStatisticsForm,
     FORMAT_JSON, FORMAT_CSV,
     DEFAULT_START_ROW, DEFAULT_NUM_ROWS)
from django.utils.decorators import method_decorator
from django.conf import settings

from ravens_metadata_apps.r_preprocess.preprocess_util import run_preprocess

def view_r_preprocess_form(request):
    """Basic test form"""
    if request.method == 'POST':
        form = PreprocessJobForm(request.POST, request.FILES)
        if form.is_valid():
            job = form.save()

            run_preprocess(job.id)

            redirect_url = reverse('view_preprocess_job_status',
                                   kwargs=dict(job_id=job.id))

            return HttpResponseRedirect(redirect_url)
    else:
        form = PreprocessJobForm()

    return render(request,
                  'r_preprocess/view_r_preprocess_form.html',
                  {'form': form})
