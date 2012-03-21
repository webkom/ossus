from django.conf.urls.defaults import patterns, include, handler500
from django.conf import settings
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns(

    '',

    (r'^$', 'app.machine.views.overview'),
    (r'^dashboard/', include('app.machine.urls')),
    (r'^machines/', include('app.machine.urls')),
    (r'^storages/', include('app.storage.urls')),
    (r'^customers/', include('app.customer.urls')),
    (r'^accounts/', include('app.accounts.urls')),
    (r'^admin/', include(admin.site.urls)),
    (r'^api/', include('api.urls')),

)

if settings.DEBUG:
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    urlpatterns += staticfiles_urlpatterns()