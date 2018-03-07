from django import forms

class MinimalPreprocessForm(forms.Form):
    """Very basic start..."""
    data_file = forms.FileField()
