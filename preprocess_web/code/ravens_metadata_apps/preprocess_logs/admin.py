from django.contrib import admin

from ravens_metadata_apps.preprocess_logs.models import LogEntry


class LogEntryAdmin(admin.ModelAdmin):
    save_on_top = True
    search_fields = ('name',)
    list_display = ('name', 'data_file',)
    readonly_fields = ('modified', 'created')

admin.site.register(LogEntry, LogEntryAdmin)
