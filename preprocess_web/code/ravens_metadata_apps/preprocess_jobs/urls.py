from django.urls import path

from ravens_metadata_apps.preprocess_jobs import views

urlpatterns = (
    # homepage/ splash page
    #
    path(r'homepage',
         views.view_homepage,
         name='view_homepage'
         ),

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
    path(r'api/update-metadata',
         views.api_update_metadata,
         name='api_update_metadata'),

    # job to retrieve preprocess data
    #
    path(r'api/metadata/<int:preprocess_id>',
         views.api_get_latest_metadata,
         name='api_get_latest_metadata'),

    # job to download preprocess
    #
    path(r'api/download_preprocess/<int:preprocess_id>',
         views.api_download,
         name='api_download'),
    # job to get detail
    #
    path(r'api/detail/<int:preprocess_id>',
         views.api_detail,
         name='api_detail'),

    # job to retrieve preprocess data version
    #
    #path(r'api/metadata/<int:job_id>/version/<int:update_id>',
    #     views.api_get_metadata_version,
    #     name='api_get_metadata_version'),

    #job to get all the preprocessed jobs
    #
    path(r'list',
         views.view_job_list,
         name='view_list'),

    # default to upload form, for now
    #
    path('hello',
         views.test_view,
         name='test_view'),

)
