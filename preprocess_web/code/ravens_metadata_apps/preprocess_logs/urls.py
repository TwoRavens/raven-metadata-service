from django.conf.urls import url
from ravens_metadata_apps.preprocess_logs import views

urlpatterns = (


    # Show saved workspaces for the logged in user
    #
    url(r'^form-basic-upload$',
        views.view_basic_upload_form,
        name='view_basic_upload_form'),

    # Show saved workspaces for the logged in user
    #
    url(r'^handle-basic-preprocess-upload$',
        views.handle_basic_preprocess_upload,
        name='handle_basic_preprocess_upload'),


    # Show saved workspaces for the logged in user
    #
    url(r'^$',
        views.view_basic_upload_form,
        name='test_view'),

)
