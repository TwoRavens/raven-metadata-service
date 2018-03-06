from django.conf.urls import url
from ravens_metadata_apps.preprocess_logs import views

urlpatterns = (

    # Show saved workspaces for the logged in user
    #
    url(r'^$',
        views.test_view,
        name='test_view'),

)
