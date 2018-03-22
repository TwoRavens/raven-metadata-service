from django import forms
from ravens_metadata_apps.preprocess_jobs.models import PreprocessJob
from django.utils.translation import gettext_lazy as _

class PreprocessJobForm(forms.ModelForm):
    """Very basic start..."""

    class Meta:
        model = PreprocessJob
        fields = ('source_file',)


FORMAT_JSON = 'json'
FORMAT_CHOICES = [(FORMAT_JSON, 'json'),
                  ('csv', 'csv')]
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
            raise forms.ValidationError(
                _('A preprocess file does not exist for id: %s' % preprocess_id))
        return preprocess_id

    def clean_start_row(self):
        """Check if PreprocessJob exists"""
        start_row = self.cleaned_data.get('start_row')
        if start_row is None:
            start_row = 1

        if start_row < 1:
            raise forms.ValidationError(
                _('The start row must be 1 or greater.'))

        return start_row

    # start row > 0
    # number_rows > 0


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
