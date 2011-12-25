from django.conf.urls.defaults import patterns, include, handler500
from django.conf import settings
from django.contrib import admin

#admin.autodiscover()

handler500 # Pyflakes

urlpatterns = patterns(

    '',

        (r'^$', 'app.dashboard.views.overview'),
        (r'^dashboard/', include('app.dashboard.urls')),
        (r'^machines/', include('app.machine.urls')),
        (r'^accounts/', include('app.accounts.urls')),
        (r'^admin/', include(admin.site.urls)),
        (r'^api/', include('api.urls')),

    )

if settings.DEBUG:
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns
    urlpatterns += staticfiles_urlpatterns()