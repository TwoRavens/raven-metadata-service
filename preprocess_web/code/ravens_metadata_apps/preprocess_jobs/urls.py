from django.urls import path, re_path

from ravens_metadata_apps.preprocess_jobs import views

urlpatterns = (
    # homepage/ splash page
    #
    path(r'homepage',
         views.view_homepage,
         name='view_homepage'),

    # Show saved workspaces for the logged in user
    #
    path(r'form-basic-upload',
         views.view_basic_upload_form,
         name='view_basic_upload_form'),

    path(r'api/process-single-file',
         views.api_process_single_file,
         name='api_process_single_file'),

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
    re_path(r'api/metadata/(?P<preprocess_id>[0-9]{1,10})',
            views.api_get_latest_metadata,
            name='api_get_latest_metadata'),

    # job to download preprocess
    #
    re_path(r'api/metadata/download/(?P<preprocess_id>[0-9]{1,10})',
            views.api_download_latest_metadata,
            name='api_download_latest_metadata'),
    # job to download preprocess version
    #
    re_path(r'api/metadata_download/(?P<preprocess_id>[0-9]{1,10})/version/(?P<version>[0-9]+\.?[0-9]*)',
            views.api_download_version,
            name='api_download_version'),

     # job to get detail
    #
    re_path(r'api/detail/(?P<preprocess_id>[0-9]{1,10})',
         views.api_detail,
         name='api_detail'),



    re_path(r'api/metadata/(?P<preprocess_id>[0-9]{1,10})/version/(?P<version>[0-9]+\.?[0-9]*)',
        views.api_get_metadata_version,
       name='api_get_metadata_version'),

    # job to retrieve preprocess data version
    #

    #job to get all the preprocessed jobs
    #
    path(r'list',
         views.view_job_list,
         name='view_list'),

    #path(r'api/metadata/<int:preprocess_id>/version/<int:version_number>',
    #     views.api_get_metadata_version,
    #     name='api_get_metadata_version'),



    # default to upload form, for now
    #
    path('hello',
         views.test_view,
         name='test_view'),

)
