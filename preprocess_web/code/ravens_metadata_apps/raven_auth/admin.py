from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from ravens_metadata_apps.raven_auth.models import User

from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.utils.translation import ugettext_lazy as _

from django.contrib.auth.forms import UserCreationForm

from ravens_metadata_apps.raven_auth.models import User

class RavenUserForm(forms.ModelForm):

    class Meta:
        model = User
        fields = '__all__'

class RavenUserAdmin(UserAdmin):

    form = RavenUserForm

    list_display = ('username', 'email',
                    'first_name', 'last_name',
                    'is_staff',
                    'api_token', 'token_updated')


admin.site.register(User, RavenUserAdmin)
