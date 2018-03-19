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

    # job info JSON format
    #
    path('job-info-json/<int:job_id>',
         views.show_job_info,
         name='show_job_info'),

    # job info HTML page
    #
    path('job-status-page/<int:job_id>',
         views.view_job_status_page,
         name='view_job_status_page'),


    # default to upload form, for now
    #
    path('hello',
        views.test_view,
        name='test_view'),

)
