from django.urls import path
from ravens_metadata_apps.content_pages import views

urlpatterns = (

    path('monitoring/alive',
        views.view_monitoring_alive,
        name='view_monitoring_alive'),

    path('err-500-test',
        views.view_err_500_test,
        name='view_err_500_test'),

    # homepage/ splash page
    #
    path('',
         views.view_homepage,
         name='view_homepage'),
)
