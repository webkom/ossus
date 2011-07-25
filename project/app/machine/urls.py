from django.conf.urls.defaults import patterns

urlpatterns = patterns('app.machine.views',
                        (r'^overview/', 'overview'),
                        (r'^(?P<id>\w+)/view/$', 'view'),
                       )