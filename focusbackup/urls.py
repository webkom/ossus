# -*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, include, handler500
from django.conf import settings
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns(
    '',
    (r'^$', 'focusbackup.app.machine.views.overview'),
    (r'^machines/', include('focusbackup.app.machine.urls')),
    (r'^schedules/', include('focusbackup.app.schedule.urls')),
    (r'^storages/', include('focusbackup.app.storage.urls')),
    (r'^docs/', include('focusbackup.app.docs.urls')),
    (r'^customers/', include('focusbackup.app.customer.urls')),
    (r'^accounts/', include('focusbackup.app.accounts.urls')),
    (r'^admin/', include(admin.site.urls)),
    (r'^api/', include('focusbackup.api.urls')),


    (r'^download_current_agent/', 'focusbackup.core.views.download_current_agent'),
    (r'^download_current_updater/', 'focusbackup.core.views.download_current_updater'),

    (r'^file/(?P<filename>.*)$', 'focusbackup.core.views.retrieve_file'),

)

if settings.DEBUG:
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    urlpatterns += staticfiles_urlpatterns()
