from django.urls import path, re_path

from ravens_metadata_apps.metadata_schemas import views

urlpatterns = (

    # Show saved workspaces for the logged in user
    #
    path(r'rst/variable-defn',
         views.view_variable_definitions,
         name='view_variable_definitions'),
)
