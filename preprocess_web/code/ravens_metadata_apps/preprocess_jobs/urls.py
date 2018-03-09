from django.urls import path

from ravens_metadata_apps.preprocess_jobs import views

urlpatterns = (

    # Show saved workspaces for the logged in user
    #
    path(r'form-basic-upload',
         views.view_basic_upload_form,
         name='view_basic_upload_form'),

    path(r'api-single-file',
         views.endpoint_api_single_file,
         name='endpoint_api_single_file'),

    # job info
    #
    path('job-info/<int:job_id>',
         views.show_job_info,
         name='show_job_info'),


    # default to upload form, for now
    #
    path('hello',
        views.test_view,
        name='test_view'),

)
