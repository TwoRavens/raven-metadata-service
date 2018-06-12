from django.contrib import admin

from ravens_metadata_apps.preprocess_jobs.models import \
    (PreprocessJob, MetadataUpdate)
from ravens_metadata_apps.dataverse_connect.models import \
    (DataverseFileInfo)
from ravens_metadata_apps.metadata_schemas.models import MetadataSchema

class DataverseFileInfoInline(admin.TabularInline):
    model = DataverseFileInfo
    #fk_name = "orig_metadata"
    #exclude = ('update_json', 'note', 'previous_update')
    readonly_fields = ('dataverse', 'datafile_id',
                       'dataset_id', 'dataset_doi',
                       'original_filename',
                       'jsonld_citation', 'formatted_citation',
                       'created', 'modified', )
    extra = 0
    can_delete = False
    show_change_link = True

class MetadataUpdateInline(admin.TabularInline):
    model = MetadataUpdate
    fk_name = "orig_metadata"
    exclude = ('update_json', 'note', 'previous_update')
    readonly_fields = ('name', 'metadata_file', 'update_data_as_json',
                       'editor', 'created', 'modified', )
    extra = 0
    can_delete = True
    show_change_link = True

class PreprocessJobAdmin(admin.ModelAdmin):
    inlines = [
        DataverseFileInfoInline,
        MetadataUpdateInline,
    ]
    save_on_top = True
    search_fields = ('name',)
    list_display = ('id',
                    'name',
                    'creator',
                    'is_success',
                    'state',
                    'schema_version',
                    'task_id',
                    'created',
                    'source_file',)

    list_filter = ('is_success',
                   'is_metadata_public',
                   'state',
                   'schema_version')

    readonly_fields = ('modified',
                       'created',
                       'source_file_path',
                       'creator')

admin.site.register(PreprocessJob, PreprocessJobAdmin)


class MetadataUpdateAdmin(admin.ModelAdmin):
    save_on_top = True
    list_display = ('id',
                    'orig_metadata',
                    'name',
                    'version_number',
                    'editor',
                    'created',
                    'modified')

    list_filter = ('version_number',
                   'editor',)

    readonly_fields = ('modified',
                       'created',
                       'metadata_file_path',
                       'editor')

admin.site.register(MetadataUpdate, MetadataUpdateAdmin)

class MetadataSchemaAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'schema_type',
        'version',
        'is_published',
        'is_latest',
        'schema_file',
        'description'
    )
    list_filter = ('version',
                   'is_latest')
admin.site.register(MetadataSchema, MetadataSchemaAdmin)
