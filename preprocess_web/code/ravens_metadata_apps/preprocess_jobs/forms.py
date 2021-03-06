import json

from django import forms
from django.conf import settings
from ravens_metadata_apps.preprocess_jobs.models import PreprocessJob
from django.utils.translation import gettext_lazy as _

class PreprocessJobForm(forms.ModelForm):
    """Very basic start..."""

    class Meta:
        model = PreprocessJob
        fields = ('source_file',)

    def __init__(self, *args, **kwargs):
        super(PreprocessJobForm, self).__init__(*args, **kwargs)
        self.fields['source_file'].widget.attrs.update(\
                    {'class' : 'form-control-file form-control'})


FORMAT_JSON = 'json'
FORMAT_CSV = 'csv'
INPUT_FORMATS = (FORMAT_JSON, FORMAT_CSV)
FORMAT_CHOICES = [(x, x) for x in INPUT_FORMATS]
VIEWABLE_TRUE = True
VIEWABLE_FALSE = False
INPUT_VIEWABLE_TYPES = (VIEWABLE_TRUE,VIEWABLE_FALSE)
VIEWABLE_CHOICES = [(x,x) for x in INPUT_VIEWABLE_TYPES]

DEFAULT_START_ROW = 1
DEFAULT_NUM_ROWS = 100


class RetrieveRowsForm(forms.Form):
    preprocessId = forms.IntegerField(label="Preprocess Id")

    startRow = forms.IntegerField(label="Start row",
                                  required=False,
                                  initial=DEFAULT_START_ROW)

    numberRows = forms.IntegerField(label="Number of rows",
                                    required=False,
                                    initial=DEFAULT_NUM_ROWS)

    format = forms.ChoiceField(choices=FORMAT_CHOICES,
                               initial=FORMAT_JSON,
                               required=False)


    def __init__(self, *args, **kwargs):
        super(RetrieveRowsForm, self).__init__(*args, **kwargs)
        for attr_name in ['preprocessId', 'startRow', 'numberRows', 'format']:
            self.fields[attr_name].widget.attrs.update(\
                            {'class' : 'form-control'})

    def clean_preprocessId(self):
        """Check if PreprocessJob exists"""
        preprocess_id = self.cleaned_data.get('preprocessId')
        try:
            job = PreprocessJob.objects.get(id=preprocess_id)
        except PreprocessJob.DoesNotExist:
            # errors.append('A preprocess file does not exist for id: %s' % preprocess_id)
            raise forms.ValidationError(
                _('A preprocess file does not exist for id: %s' % preprocess_id))

        return preprocess_id

    def clean_startRow(self):
        """Check if start row is valid"""
        start_row = self.cleaned_data.get('startRow')
        if start_row is None:
            start_row = 1

        if start_row < 1:
            # errors.append('The start row must be 1 or greater.')
            raise forms.ValidationError(
                _('The start row must be 1 or greater.'))

        return start_row

    def clean_numberRows(self):
        """Check if number_rows is valid"""
        number_rows = self.cleaned_data.get('numberRows')

        if number_rows is None:
            number_rows = DEFAULT_NUM_ROWS

        if number_rows < 1:
            # errors.append(forms.ValidationError)
            raise forms.ValidationError(
                _('The number of rows must be 1 or greater.'))
        elif number_rows > settings.MAX_SOURCE_FILE_ROWS_TO_RETRIEVE:
            raise forms.ValidationError(
                _('The number cannot be greater than %d.') % \
                settings.MAX_SOURCE_FILE_ROWS_TO_RETRIEVE)

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

class CustomStatisticsForm(forms.Form):
    """ this class takes the custom statistics update form:
                [
             {
               "id": 1,
               "name": "Third order statistic",
               "variables": ["lpop"], _optional_
               "image": "image_id", _optional_
               "value": "23.45",
               "description": "Third smallest value",
               "replication": "sorted(X)[2]",
               "omit": false _optional_
             },
             {*custom statistic 2*},
             ...
            ]
    """

    # single custom_statistic info
    name = forms.CharField(required= True, label='Name')
    variables = forms.CharField(required=True, label='Variables')
    image = forms.CharField(required=False, label='Image')
    value = forms.CharField(required= True, label='Value')
    description = forms.CharField(required=False, label='Description')
    replication = forms.CharField(required= False,label='replication')
    viewable = forms.NullBooleanField(required=False,initial=False)
    # omit = forms.ChoiceField(choices=OMIT_CHOICES,
    #                           initial=OMIT_FALSE,
    #                           required=True)

    # def clean_preprocess_id(self):
    #     """Check if PreprocessJob exists"""
    #     preprocess_id = self.cleaned_data.get('preprocess_id')
    #     try:
    #         job = PreprocessJob.objects.get(id=preprocess_id)
    #     except PreprocessJob.DoesNotExist:
    #         # errors.append('A preprocess file does not exist for id: %s' % preprocess_id)
    #         raise forms.ValidationError(
    #             _('A preprocess file does not exist for id: %s' % preprocess_id))
    #
    #     return preprocess_id

    def clean_name(self):
        name = self.cleaned_data.get('name')

        return name

    def clean_variables(self):
        variable = self.cleaned_data.get('variables')

        return [x.strip() for x in variable.split(',')]

    def clean_image(self):
        image = self.cleaned_data.get('image')

        if image is None:
            # image = 'preprocess_web/code/static/images/TwoRavens.png'
            return []

        return [x.strip() for x in image.split(',')]

    def clean_value(self):
        value = self.cleaned_data.get('value')

        return value

    def clean_description(self):
        desc = self.cleaned_data.get('description')

        return desc

    def clean_replication(self):
        rep = self.cleaned_data.get('replication')

        return rep

    def clean_viewable(self):
        """ check if the format is valid"""
        input_viewable = self.cleaned_data.get('viewable')
        if not input_viewable:
            input_viewable = False

        return input_viewable

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

"""
python manage.py shell

from ravens_metadata_apps.preprocess_jobs.forms import CustomStatisticsForm
import json

json_str ='''

    {
   "preprocess_id":1677,
   "name":"Third order statistic",
   "variables":"lpop,bebop",
   "image":"http://www.google.com",
   "value":23.45,
   "description":"Third smallest value",
   "replication":"sorted(X)[2]",
   "omit":"true"
}'''

form_data = json.loads(json_str)

f = CustomStatisticsForm(form_data)
if f.is_valid():
    print(f.cleaned_data)
else:
    print(f.errors())


"""
