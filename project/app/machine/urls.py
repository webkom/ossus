from django.conf.urls.defaults import patterns

urlpatterns = patterns('app.machine.views',
                        (r'^$', 'overview'),
                        (r'^new/$', 'new'),
                        (r'^(?P<id>\w+)/view/$', 'view'),
                        (r'^(?P<id>\w+)/edit/$', 'edit'),
)