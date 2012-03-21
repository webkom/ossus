from django.conf.urls.defaults import patterns

urlpatterns = patterns('app.storage.views',
    (r'^$', 'overview'),
    (r'^new/$', 'new'),
    (r'^(?P<id>\w+)/view/$', 'edit'),
    (r'^(?P<id>\w+)/edit/$', 'edit'),
)