import warnings

from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.utils.deprecation import RemovedInDjango21Warning


class LoginViewExtraContext(LoginView):
    """Subclass the Django LoginView to add extra context data"""

    def get_context_data(self, **kwargs):
        """Add extra context here"""
        context = super().get_context_data(**kwargs)


        # add variable checking for the d3m_domain
        #
        context['just_logged_out'] = 'just_logged_out' in self.request.GET

        return context
