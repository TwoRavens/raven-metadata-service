from django.urls import path, re_path

from ravens_metadata_apps.r_preprocess import \
 (views,)

urlpatterns = (

    # Upload file through form and run *R* preprocess
    #
    path(r'run-in-queue',
         views.view_r_preprocess_form,
         name='view_r_preprocess_form'),

    path(r'api-run-in-queue',
         views.api_r_preprocess_form,
         name='api_r_preprocess_form'),

    path(r'run-direct',
         views.view_r_preprocess_form_direct,
         name='view_r_preprocess_form_direct'),

)
