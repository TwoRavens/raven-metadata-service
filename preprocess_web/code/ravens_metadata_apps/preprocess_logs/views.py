from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from django.http import JsonResponse, HttpResponse, Http404, HttpResponseRedirect
from django.contrib.auth.decorators import login_required

from basic_preprocess import preprocess_csv_file
from random_util import get_alphanumeric_lowercase

from .forms import MinimalPreprocessForm

# Create your views here.
def test_view(request):
    return HttpResponse('hello')


def view_basic_upload_form(request):
    """Basic test form"""
    info_dict = dict()

    return render(request,
                  'preprocess/view_basic_upload_form.html',
                  info_dict)


def handle_basic_preprocess_upload(request):
    """Endpoint to upload file, send it to the preprocess queue, and return
    a callback url to check progress"""
    if not request.POST:
        return HttpResponse('Not file submitted.  Please use a POST',
                            status=412)

    form = MinimalPreprocessForm(request.POST)
    if not form.is_valid():
        return HttpResponse('Not file uploaded',
                            status=412)

    # ---------------------
    # upload file
    # ---------------------
    """request.FILES['data_file']
    with open('/tmp/file/name.txt', 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

            handle_uploaded_file(request.FILES['file'])
            return HttpResponseRedirect('/success/url/')
    """
    return HttpResponse('handle_basic_preprocess_upload')
