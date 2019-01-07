from django.urls import path, re_path

from ravens_metadata_apps.r_preprocess import \
 (views,)

urlpatterns = (

    # Upload file through form and run *R* preprocess
    #
    path(r'test-run',
         views.view_r_preprocess_form,
         name='view_r_preprocess_form'),
)
