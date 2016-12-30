from __future__ import absolute_import, unicode_literals
import os

from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic import TemplateView

from wagtail.wagtailadmin import urls as wagtailadmin_urls
from wagtail.wagtailcore import urls as wagtail_urls
from wagtail.wagtaildocs import urls as wagtaildocs_urls
from wagtail.contrib.wagtailsitemaps.views import sitemap


if os.getenv('PROD') == 'True':
    urlpatterns = [
        url(r'^django-JN4G0zjF/', include(admin.site.urls)),
        url(r'^JN4G0zjF/', include(wagtailadmin_urls)),
    ]
else:
    urlpatterns = [
        url(r'^django-admin/', include(admin.site.urls)),
        url(r'^admin/', include(wagtailadmin_urls)),
    ]

urlpatterns += [
    url(r'^documents/', include(wagtaildocs_urls)),

    url('^sitemap\.xml$', sitemap),
    url(r'^robots\.txt/$', TemplateView.as_view(template_name='robots.txt', content_type='text/plain')),

    url(r'', include(wagtail_urls)),
]

if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    # Serve static and media files from development server
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
