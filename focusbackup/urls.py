# -*- coding: utf-8 -*-
from django.conf import settings
from django.conf.urls import patterns, include
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

admin.autodiscover()

urlpatterns = patterns(
    '',
    (r'^$', 'focusbackup.app.machine.views.overview'),
    (r'^accounts/', include('focusbackup.app.accounts.urls')),
    (r'^machines/', include('focusbackup.app.machine.urls')),
    (r'^backups/', include('focusbackup.app.backup.urls')),
    (r'^storages/', include('focusbackup.app.storage.urls')),
    (r'^customers/', include('focusbackup.app.customer.urls')),
    (r'^admin/', include(admin.site.urls)),
    (r'^api/', include('focusbackup.api.urls')),

    (r'^download_current_agent/', 'focusbackup.core.views.download_current_agent'),
    (r'^download_current_updater/', 'focusbackup.core.views.download_current_updater'),

    (r'^file/(?P<filename>.*)$', 'focusbackup.core.views.retrieve_file'),

)

urlpatterns += staticfiles_urlpatterns()

#urlpatterns += patterns('',
#                        (r'^uploads/(?P<path>.*)$', 'django.views.static.serve',
#                         {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
#)