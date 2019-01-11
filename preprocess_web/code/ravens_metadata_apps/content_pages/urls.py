from django.urls import path
from ravens_metadata_apps.content_pages import views

urlpatterns = (

    path('monitoring/alive',
         views.view_monitoring_alive,
         name='view_monitoring_alive'),

    path('test/err-500',
         views.view_err_500_test,
         name='view_err_500_test'),

    path('test/err-400',
         views.view_err_404_test,
         name='view_err_404_test'),

    path('datamart-page',
         views.view_datamart_page,
         name='view_datamart_page'),

    # homepage/ splash page
    #
    path('',
         views.view_homepage,
         name='view_homepage'),
)
