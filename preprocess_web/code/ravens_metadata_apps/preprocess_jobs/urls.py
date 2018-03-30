from django.urls import path

from ravens_metadata_apps.preprocess_jobs import views

urlpatterns = (

    # Show saved workspaces for the logged in user
    #
    path(r'form-basic-upload',
         views.view_basic_upload_form,
         name='view_basic_upload_form'),

    path(r'api/process-single-file',
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

    # job to retrieve rows
    #
    path(r'form/retrieve-rows',
         views.view_retrieve_rows_form,
         name='view_form_retrieve_rows'),

    # job to retrieve rows
    #
    path(r'api/retrieve-rows',
         views.view_api_retrieve_rows,
         name='view_api_retrieve_rows'),

    # job to retrieve rows
    #
    path(r'editor',
         views.variable_display_endpoint,
         name='view_editor'),


    # default to upload form, for now
    #
    path('hello',
         views.test_view,
         name='test_view'),

)
