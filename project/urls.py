from django.conf.urls.defaults import patterns, include, handler500
from django.conf import settings
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns(
    '',
    (r'^$', 'app.machine.views.overview'),
    (r'^machines/', include('app.machine.urls')),
    (r'^schedules/', include('app.schedule.urls')),
    (r'^storages/', include('app.storage.urls')),
    (r'^docs/', include('app.docs.urls')),
    (r'^customers/', include('app.customer.urls')),
    (r'^accounts/', include('app.accounts.urls')),
    (r'^admin/', include(admin.site.urls)),
    (r'^api/', include('api.urls')),


    (r'^download_current_agent/', 'core.views.download_current_agent'),
    (r'^download_current_updater/', 'core.views.download_current_updater'),

    (r'^file/(?P<filename>.*)$', 'core.views.retrieve_file'),

)

if settings.DEBUG:
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns
    urlpatterns += staticfiles_urlpatterns()
