import json

from django import forms
from ravens_metadata_apps.preprocess_jobs.models import PreprocessJob
from django.utils.translation import gettext_lazy as _

class PreprocessJobForm(forms.ModelForm):
    """Very basic start..."""

    class Meta:
        model = PreprocessJob
        fields = ('source_file',)


FORMAT_JSON = 'json'
FORMAT_CSV = 'csv'
INPUT_FORMATS = (FORMAT_JSON, FORMAT_JSON)
FORMAT_CHOICES = [(x, x) for x in INPUT_FORMATS]
# errors = []


class RetrieveRowsForm(forms.Form):

    preprocess_id = forms.IntegerField()
    start_row = forms.IntegerField(required=False)
    number_rows = forms.IntegerField(required=False,
                                     initial=100)
    format = forms.ChoiceField(choices=FORMAT_CHOICES,
                               initial=FORMAT_JSON,
                               required=False)


    def clean_preprocess_id(self):
        """Check if PreprocessJob exists"""
        preprocess_id = self.cleaned_data.get('preprocess_id')
        try:
            job = PreprocessJob.objects.get(id=preprocess_id)
        except PreprocessJob.DoesNotExist:
            # errors.append('A preprocess file does not exist for id: %s' % preprocess_id)
            raise forms.ValidationError(
                _('A preprocess file does not exist for id: %s' % preprocess_id))

        return preprocess_id

    def clean_start_row(self):
        """Check if start row is valid"""
        start_row = self.cleaned_data.get('start_row')
        if start_row is None:
            start_row = 1

        if start_row < 1:
            # errors.append('The start row must be 1 or greater.')
            raise forms.ValidationError(
                _('The start row must be 1 or greater.'))

        return start_row

    def clean_number_rows(self):
        """Check if number_rows is valid"""
        number_rows = self.cleaned_data.get('number_rows')
        if number_rows is None:
            number_rows = 100   # later on it would be the maximum number of rows in the source file

        if number_rows < 1:
            # errors.append(forms.ValidationError)
            raise forms.ValidationError(
                _('The number of rows must be 1 or greater.'))

        return number_rows

    def clean_format(self):
        """ check if the format is valid"""
        input_format = self.cleaned_data.get('format')
        if not input_format:
            input_format = FORMAT_JSON

        if input_format not in INPUT_FORMATS:
            # errors.append(forms.ValidationError)
            raise forms.ValidationError(
                _('The format should be either json or csv.'))

        return input_format

# errors = json.dumps(errors)
"""
fab run_shell
from ravens_metadata_apps.preprocess_jobs.forms import RetrieveRowsForm

data = dict(preprocess_id=1,
            start_row=10,
            format='json')
f = RetrieveRowsForm(data)
f.is_valid()
f.errors

"""
