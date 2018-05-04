from django.shortcuts import render
from django.urls import reverse

from django.http import \
    (HttpResponseRedirect) #(JsonResponse, HttpResponse, Http404, QueryDict)
from ravens_metadata_apps.dataverse_connect.forms import \
    (DataverseFileByURLForm, DataverseFileByIdForm)
#from ravens_metadata_apps.dataverse_connect.tasks import \
#    (preprocess_dataverse_file)
from ravens_metadata_apps.dataverse_connect.dataverse_util import \
    (DataverseUtil)


def view_dataverse_file_form(request):
    """Process a Dataverse File form: 2 possible forms"""
    form_by_url = None
    form_by_id = None
    if request.method == 'POST':
        # Try each of the forms...
        #
        if 'dataverse_file_url' in request.method.POST:
            # try form 1
            #
            form_by_url = DataverseFileByURLForm(request.POST)
            if form_by_url.is_valid():
                job = DataverseUtil.process_dataverse_file(\
                            form_by_url.get_dataverse_file_url())

                redirect_url = reverse('view_preprocess_job_status',
                                       kwargs=dict(job_id=job.id))

                return HttpResponseRedirect(redirect_url)

        else:
            form_by_id = DataverseFileByIdForm(request.POST)
            if form_by_id.is_valid():
                job = DataverseUtil.process_dataverse_file(\
                            form_by_id.get_dataverse_file_url())

                redirect_url = reverse('view_preprocess_job_status',
                                       kwargs=dict(job_id=job.id))

                return HttpResponseRedirect(redirect_url)

    # If there an error or no POST, create the forms as needed....
    #
    if not form_by_id:
        form_by_id = DataverseFileByIdForm()

    if not form_by_url:
        form_by_url = DataverseFileByURLForm()

    info_dict = dict(form_by_id=form_by_id,
                     form_by_url=form_by_url)

    return render(request,
                  'dataverse_connect/view_dataverse_file_form.html',
                  info_dict)
