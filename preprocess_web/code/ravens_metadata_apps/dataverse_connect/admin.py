from django.contrib import admin

from ravens_metadata_apps.dataverse_connect.models import RegisteredDataverse



class RegisteredDataverseAdmin(admin.ModelAdmin):
    """For RegisteredDataverse objects"""
    search_fields = ('name', 'dataverse_url', 'notes')
    list_display = ('name', 'dataverse_url', 'active', 'notes')
    save_on_top = True
    list_filter = ('active', )

admin.site.register(RegisteredDataverse, RegisteredDataverseAdmin)
