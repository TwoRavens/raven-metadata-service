from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse, Http404#, HttpResponseRedirect
from ravens_metadata_apps.utils.view_helper import get_json_success
from django.conf import settings


def view_homepage(request):
    """landing page"""
    return render(request,
                  'preprocess/homepage.html',
                  {'HIDE_HOME_BUTTON':True,
                   'TEST_ENV_VARIABLE': settings.TEST_ENV_VARIABLE})

def view_monitoring_alive(request):
    """For kubernetes liveness check"""
    return JsonResponse(get_json_success("server up"))


@login_required
def view_err_500_test(request):
    """Force a 500 error"""

    5 / 0 # div by 0, uh oh

    return HttpResponse('never reaches')

@login_required
def view_err_404_test(request):
    """Force a 404 error"""

    raise Http404('view_err_404_test')
