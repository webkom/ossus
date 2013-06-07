from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('focusbackup.app.machine.views',
                        url(r'^$', 'overview', name="machine_overview"),
                        (r'^new/$', 'new'),
                        url(r'^(?P<id>\w+)/view/$', 'view', name="view_machine"),
                        (r'^(?P<id>\w+)/edit/$', 'edit'),
)