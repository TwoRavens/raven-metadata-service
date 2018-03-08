from django.contrib import admin

from ravens_metadata_apps.preprocess_jobs.models import PreprocessJob


class PreprocessJobAdmin(admin.ModelAdmin):
    save_on_top = True
    search_fields = ('name',)
    list_display = ('id',
                    'name',
                    'state',
                    'schema_version',
                    'task_id',
                    'created',
                    'source_file',)
    list_filter = ('state',
                   'schema_version')
    readonly_fields = ('modified',
                       'created',
                       'source_file_path')

admin.site.register(PreprocessJob, PreprocessJobAdmin)
