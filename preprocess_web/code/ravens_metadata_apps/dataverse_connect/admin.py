from django.contrib import admin

from ravens_metadata_apps.dataverse_connect.models import \
    DataverseFileInfo, RegisteredDataverse
from ravens_metadata_apps.preprocess_jobs.models import \
    PreprocessJob


class DataverseFileInfoAdmin(admin.ModelAdmin):
    """For RegisteredDataverse objects"""
    search_fields = ('dataverse__name', 'dataset_doi')
    list_display = ('datafile_id', 'dataverse',
                    'dataset_id', 'dataset_doi',
                    'original_filename', 'preprocess_job')
    readonly_fields = ('created', 'modified')
    save_on_top = True
    list_filter = ('dataverse', )
admin.site.register(DataverseFileInfo, DataverseFileInfoAdmin)


class RegisteredDataverseAdmin(admin.ModelAdmin):
    """For RegisteredDataverse objects"""
    search_fields = ('name', 'dataverse_url', 'notes')
    list_display = ('name', 'dataverse_url', 'active', 'notes')
    readonly_fields = ('created', 'modified')
    save_on_top = True
    list_filter = ('active', )
admin.site.register(RegisteredDataverse, RegisteredDataverseAdmin)
