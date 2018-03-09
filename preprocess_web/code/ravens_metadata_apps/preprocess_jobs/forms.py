from django import forms
from ravens_metadata_apps.preprocess_jobs.models import PreprocessJob

class PreprocessJobForm(forms.ModelForm):
    """Very basic start..."""
    
    class Meta:
        model = PreprocessJob
        fields = ('source_file',)
