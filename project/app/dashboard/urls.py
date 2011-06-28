from django.conf.urls.defaults import patterns

urlpatterns = patterns('app.dashboard.views',
                        (r'^overview/', 'overview'),
                        (r'^(?P<machine_id>\w+)/view/$', 'view_machine'),
                       )