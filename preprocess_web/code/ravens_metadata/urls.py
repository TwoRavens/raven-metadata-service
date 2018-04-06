"""ravens_metadata URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from django.views.generic import RedirectView
from django.conf import settings
from django.conf.urls.static import static

admin.site.site_header = 'TwoRavens Metadata Service'
admin.site.index_title = 'Features area'
admin.site.site_title = 'TwoRavens Metadata Service'

urlpatterns = [

<<<<<<< HEAD
    path(r'preprocess/', include('ravens_metadata_apps.preprocess_jobs.urls')),
    path(r'auth/', include('ravens_metadata_apps.raven_auth.urls')),
=======
    path('preprocess/', include('ravens_metadata_apps.preprocess_jobs.urls')),

    path('api/', include('ravens_metadata_apps.api_docs.urls')),

>>>>>>> master
    path('admin/', admin.site.urls),

    # temp path until there's a home page
    path(r'', RedirectView.as_view(\
                pattern_name='view_homepage',
                permanent=False)),
                
] + static(settings.STATIC_URL,
           #document_root=settings.STATIC_ROOT)
           document_root=settings.TEST_DIRECT_STATIC)
