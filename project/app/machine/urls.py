from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('app.machine.views',
                        url(r'^$', 'overview', name="machine_overview"),
                        (r'^new/$', 'new'),
                        (r'^(?P<id>\w+)/view/$', 'view'),
                        (r'^(?P<id>\w+)/edit/$', 'edit'),
)