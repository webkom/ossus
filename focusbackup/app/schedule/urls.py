from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('focusbackup.app.schedule.views',
    url(r'^new/(?P<machine_id>\w+)/$', 'new'),
    url(r'^(?P<machine_id>\w+)/(?P<id>\w+)/edit/$', 'edit'),
)