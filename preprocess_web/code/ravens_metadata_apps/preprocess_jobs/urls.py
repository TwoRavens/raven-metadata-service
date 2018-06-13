from django.urls import path, re_path

from ravens_metadata_apps.preprocess_jobs import views, views_api
from ravens_metadata_apps.dataverse_connect import views as dv_connect_views
from ravens_metadata_apps.metadata_schemas import views as schema_views

urlpatterns = (

    # Show saved workspaces for the logged in user
    #
    path(r'api/schema/metadata/latest',
         schema_views.view_latest_metadata_schema,
         name='view_latest_metadata_schema'),

    # Validate preprocess metadata with schema
    #
    re_path(r'api/schema/metadata/validate/(?P<preprocess_id>[0-9]{1,10})',
         schema_views.validate_preprocess,
         name='validate_preprocess'),

    # Show saved workspaces for the logged in user
    #
    re_path(r'api/schema/metadata/version/(?P<version>[a-zA-Z0-9_]+$)',
         schema_views.view_metadata_schema_version,
         name='view_metadata_schema_version'),

    # Show saved workspaces for the logged in user
    #
    path(r'api/schema/metadata/dataset/latest',
         schema_views.view_latest_dataset_schema,
         name='view_latest_dataset_schema'),

    # Show saved workspaces for the logged in user
    #
    path(r'form-basic-upload',
         views.view_basic_upload_form,
         name='view_basic_upload_form'),

    # Dataverse file form
    #
    path(r'dataverse-form',
         dv_connect_views.view_dataverse_file_form,
         name='view_dataverse_file_form'),


    # job info JSON format
    #
    path('job-info-json/<int:job_id>',
         views.show_job_info,
         name='show_job_info'),

    # job info HTML page
    #
    path('view-job-status/<int:job_id>',
         views.view_preprocess_job_status,
         name='view_preprocess_job_status'),

    # job to retrieve rows
    #
    path(r'form/retrieve-rows',
         views.view_retrieve_rows_form,
         name='view_form_retrieve_rows'),

    # job for custom statistics (add)
    #
    path(r'form/custom-statistics',
         views.view_custom_statistics_form,
         name='view_form_custom_statistics'),

    # job for custom statistics (update)
    #
    path(r'form/custom-statistics-update',
         views.view_custom_statistics_update,
         name='view_form_custom_statistics_update'),

    # job for custom statistics (delete)
    #
    path(r'form/custom-statistics-delete',
         views.view_custom_statistics_delete,
         name='view_form_custom_statistics_delete'),

    # View PreprocessJob detail, includes MetadataUpdate objects
    #
    re_path(r'detail/(?P<preprocess_id>[0-9]{1,10})',
            views.view_job_versions,
            name='view_job_versions'),


    # View list of all the preprocessed jobs
    #
    path(r'job-list',
         views.view_job_list,
         name='view_job_list'),


    path(r'api/process-single-file',
         views_api.api_process_single_file,
         name='api_process_single_file'),

    # job to retrieve rows
    #
    path(r'api/retrieve-rows',
         views_api.view_api_retrieve_rows,
         name='view_api_retrieve_rows'),

    # job to retrieve rows
    #
    path(r'api/update-metadata',
         views_api.api_update_metadata,
         name='api_update_metadata'),

    # job to retrieve preprocess job status....
    #
    re_path(r'api/metadata/(?P<preprocess_id>[0-9]{1,10})$',
            views_api.api_get_latest_metadata,
            name='api_get_latest_metadata'),


    # job to retrieve preprocess job status....
    #
    #re_path(r'api/metadata/dataverse/(?P<dataverse_file_id>[0-9]{1,11})$',
    #        views_api.api_get_latest_metadata_by_dataverse,
    #        name='api_get_latest_metadata_by_dataverse'),


    # job to retrieve preprocess data--assumes job has completed ok
    #
    path('api/job-status/<int:preprocess_id>',
         views_api.api_get_job_status,
         name='api_get_job_status'),

    # job info JSON format
    #
    path('api/job-status/<int:preprocess_id>/with-html',
         views_api.api_get_job_status_with_html,
         name='api_get_job_status_with_html'),


    # job to download preprocess
    #
    re_path(r'api/metadata/download/(?P<preprocess_id>[0-9]{1,10})',
            views_api.api_download_latest_metadata,
            name='api_download_latest_metadata'),

    # job to download preprocess version
    #
    re_path((r'api/metadata_download/(?P<preprocess_id>[0-9]{1,10})/'
             r'version/(?P<version>[0-9]+\.?[0-9]*)'),
            views_api.api_download_version,
            name='api_download_version'),


    re_path(r'api/metadata/(?P<preprocess_id>[0-9]{1,10})/version/(?P<version>[0-9]+\.?[0-9]*)',
            views_api.api_get_metadata_version,
            name='api_get_metadata_version'),



    #path(r'api/metadata/<int:preprocess_id>/version/<int:version_number>',
    #     views.api_get_metadata_version,
    #     name='api_get_metadata_version'),

    # default to upload form, for now
    #
    path('hello',
         views.test_view,
         name='test_view'),

)
