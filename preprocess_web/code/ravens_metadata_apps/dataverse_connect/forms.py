import json

from django import forms
from django.conf import settings
from django.utils.translation import gettext_lazy as _

from ravens_metadata_apps.dataverse_connect.models import RegisteredDataverse

FORM_KEY_DV_FILE_URL = 'id_dataverse_file_url'

class DataverseFileByURLForm(forms.Form):

    dataverse_file_url = forms.URLField()

    def get_dataverse_file_url(self):
        """Return the dataverse_file_url"""
        assert self.is_valid(), \
            "You must check 'is_valid()' before calling this method"
        return self.cleaned_data['dataverse_file_url']

class DataverseFileByIdForm(forms.Form):

    dataverse = forms.ModelChoiceField(\
                    queryset=RegisteredDataverse.objects.filter(active=True),
                    empty_label=('------'))
    dataverse_file_id = forms.IntegerField()

    def get_dataverse_file_url(self):
        """Return the dataverse_file_url"""
        assert self.is_valid(), \
            "You must check 'is_valid()' before calling this method"

        registered_dv = self.cleaned_data['dataverse']
        file_id = self.cleaned_data['dataverse_file_id']

        return registered_dv.get_file_access_url(file_id)


    #def clean_preprocess_id(self):
    #    """Check if PreprocessJob exists"""
    #    try:
    #        job = PreprocessJob.objects.get(id=preprocess_id)
    #    except PreprocessJob.DoesNotExist:
    #        # errors.append('A preprocess file does not exist for id: %s' % preprocess_id)
    #        raise forms.ValidationError(
    #            _('A preprocess file does not exist for id: %s' % preprocess_id))
    #
    #    return preprocess_id
