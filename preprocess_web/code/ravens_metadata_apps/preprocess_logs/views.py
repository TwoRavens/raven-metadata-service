from django.shortcuts import render
import json
from collections import OrderedDict
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.cache import never_cache

from django.http import JsonResponse, HttpResponse, Http404, HttpResponseRedirect
from django.contrib.auth.decorators import login_required

from basic_preprocess import preprocess_csv_file
from random_util import get_alphanumeric_lowercase

# Create your views here.
def test_view(request):
    return HttpResponse('hello')
