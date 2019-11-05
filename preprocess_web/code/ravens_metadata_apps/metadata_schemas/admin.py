from django.contrib import admin
from ravens_metadata_apps.metadata_schemas.models import MetadataSchema
# Register your models here.


class MetadataSchemaFile(admin.ModelAdmin):
    model = MetadataSchema

    list_display = (
        'name',
        'schema_type',
        'version',
        'is_published',
        'is_latest',
        #'schema_json',
        'description'
    )
    list_filter = ('version',
                   'is_latest')
