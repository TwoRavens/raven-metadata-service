from django.conf.urls import url
from ravens_metadata_apps.api_docs import views_swagger

urlpatterns = (

    url(r'^v1/swagger.yml$',
        views_swagger.view_swagger_doc_v1,
        name='view_swagger_doc_v1'),

)
