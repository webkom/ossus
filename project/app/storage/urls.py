from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('app.storage.views',

    url(r'^$', 'overview', name="storage_overview"),
    (r'^new/$', 'new'),
    (r'^(?P<id>\w+)/view/$', 'edit'),
    (r'^(?P<id>\w+)/edit/$', 'edit'),
)