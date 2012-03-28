from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('app.schedule.views',
    (r'^new/(?P<machine_id>\w+)/$', 'new'),
    (r'^(?P<machine_id>\w+)/(?P<id>\w+)/edit/$', 'edit'),
)