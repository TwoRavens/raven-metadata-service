from django.shortcuts import render
from django.urls import reverse

from django.conf import settings
from django.http import \
    (HttpResponseRedirect) #(JsonResponse, HttpResponse, Http404, QueryDict)
from ravens_metadata_apps.dataverse_connect.forms import \
    (DataverseFileByURLForm, DataverseFileByIdForm,
     FORM_KEY_DV_FILE_URL)
from ravens_metadata_apps.dataverse_connect.models import RegisteredDataverse
from ravens_metadata_apps.dataverse_connect.dataverse_util import \
    (DataverseUtil)


QUERY_STR_KEY_DV_FILE_URL = 'dv_file_url'
FORM_KEY_DV_FILE_URL = 'dataverse_file_url'
PRESS_SCRIPTLET_SUBMIT = 'PRESS_SCRIPTLET_SUBMIT'

def view_dataverse_file_form(request):
    """Process a Dataverse File form: 2 possible forms"""
    form_by_url = None
    form_by_id = None

    active_dvs = RegisteredDataverse.objects.filter(active=True)

    info_dict = dict(title='Create Summary Statistics for a Dataverse File',
                     SWAGGER_HOST=settings.SWAGGER_HOST,
                     SITE_SCHEME=settings.SITE_SCHEME,
                     PRESS_SCRIPTLET_SUBMIT=False,
                     active_dvs=active_dvs)



    if request.method == 'POST':
        # Try each of the forms...
        #
        if 'dataverse_file_url' in request.POST:
            # try form 1
            #
            form_by_url = DataverseFileByURLForm(request.POST)
            if form_by_url.is_valid():
                job = DataverseUtil.process_dataverse_file(\
                            form_by_url.get_dataverse_file_url())

                if not job.success:
                    info_dict['form_by_url_err_msg'] = job.err_msg
                else:
                    job_id = job.result_obj.id
                    redirect_url = reverse(\
                                       'view_preprocess_job_status',
                                       kwargs=dict(job_id=job_id))

                    return HttpResponseRedirect(redirect_url)

        else:
            form_by_id = DataverseFileByIdForm(request.POST)
            if form_by_id.is_valid():
                job = DataverseUtil.process_dataverse_file(\
                            form_by_id.get_dataverse_file_url())

                if not job.success:
                    info_dict['form_by_url_err_msg'] = job.err_msg
                else:
                    job_id = job.result_obj.id
                    redirect_url = reverse(\
                                       'view_preprocess_job_status',
                                       kwargs=dict(job_id=job_id))

                    return HttpResponseRedirect(redirect_url)

    # If there an error or no POST, create the forms as needed....
    #
    if not form_by_id:
        form_by_id = DataverseFileByIdForm()

    if not form_by_url:
        if QUERY_STR_KEY_DV_FILE_URL in request.GET:
            info_dict[FORM_KEY_DV_FILE_URL] = request.GET[QUERY_STR_KEY_DV_FILE_URL]
            info_dict[PRESS_SCRIPTLET_SUBMIT] = True

            form_by_url = DataverseFileByURLForm(info_dict)
        else:
            form_by_url = DataverseFileByURLForm()

    info_dict['form_by_id'] = form_by_id
    info_dict['form_by_url'] = form_by_url

    return render(request,
                  'dataverse_connect/view_dataverse_file_form.html',
                  info_dict)
