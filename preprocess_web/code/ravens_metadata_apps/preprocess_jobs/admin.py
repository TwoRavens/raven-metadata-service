from django.contrib import admin

from ravens_metadata_apps.preprocess_jobs.models import \
    (PreprocessJob, MetadataUpdate)


class PreprocessJobAdmin(admin.ModelAdmin):
    save_on_top = True
    search_fields = ('name',)
    list_display = ('id',
                    'name',
                    'creator',
                    'state',
                    'schema_version',
                    'task_id',
                    'created',
                    'source_file',)

    list_filter = ('is_metadata_public',
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
                    'name',
                    'editor',
                    'created',
                    'modified')

    list_filter = ('editor',)

    readonly_fields = ('modified',
                       'created',
                       'metadata_file_path',
                       'editor')

admin.site.register(MetadataUpdate, MetadataUpdateAdmin)
