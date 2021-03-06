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
from django.urls import path, re_path
from django.conf.urls import include
from django.views.generic import RedirectView
from django.conf import settings
from django.views.static import serve

admin.site.site_header = 'TwoRavens Metadata Service'
admin.site.index_title = 'Features area'
admin.site.site_title = 'TwoRavens Metadata Service'

urlpatterns = [
    #path(r'preprocess/', include('ravens_metadata_apps.preprocess_jobs.urls')),
    #path(r'auth/', include('ravens_metadata_apps.raven_auth.urls')),

    path('preprocess/', include('ravens_metadata_apps.preprocess_jobs.urls')),

    # path('r-preprocess/', include('ravens_metadata_apps.r_preprocess.urls')),

    # path('api/', include('ravens_metadata_apps.api_docs.urls')),

    path('metadata/', include('ravens_metadata_apps.metadata_schemas.urls')),

    path('admin/', admin.site.urls),

    path('', include('ravens_metadata_apps.content_pages.urls')),

]

print('TEST_DIRECT_STATIC', settings.TEST_DIRECT_STATIC)
print('STATIC_URL', settings.STATIC_URL)
if settings.DEBUG:
    urlpatterns += [
        re_path(r'^static/(?P<path>.*)$', serve, {
            'document_root': settings.TEST_DIRECT_STATIC,
            'show_indexes': True
        }),
    ]


if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        re_path(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
