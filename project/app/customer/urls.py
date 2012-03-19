from django.conf.urls.defaults import patterns

urlpatterns = patterns('app.customer.views',
    (r'^$', 'overview'),
    (r'^new/$', 'create'),
    (r'^(?P<id>\w+)/view/$', 'view'),
    (r'^(?P<id>\w+)/edit/$', 'edit'),
)