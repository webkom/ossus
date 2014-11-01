# -*- coding: utf-8 -*-
from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^$', 'focusbackup.app.machine.views.overview'),
    url(r'^machines/', include('focusbackup.app.machine.urls')),
    url(r'^backups/', include('focusbackup.app.backup.urls')),
    url(r'^storages/', include('focusbackup.app.storage.urls')),
    url(r'^customers/', include('focusbackup.app.customer.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/', include('focusbackup.api.urls')),

    url(r'^download_current_agent/', 'focusbackup.core.views.download_current_agent'),
    url(r'^download_current_updater/', 'focusbackup.core.views.download_current_updater'),
    url(r'^download_current_installer/', 'focusbackup.core.views.download_current_installer'),
)

if 'nopassword' in settings.INSTALLED_APPS:
    urlpatterns += patterns('', url(r'^accounts/', include('nopassword.urls')))
else:
    urlpatterns += patterns('', url(r'^accounts/', include('focusbackup.app.accounts.urls')))

urlpatterns += staticfiles_urlpatterns()
