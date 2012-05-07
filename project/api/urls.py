from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('api.views.machines',

    (r'^machines/$', 'get_machines'),
    (r'^machines/(?P<machine_id>\w+)/$', 'get_machines'),
    (r'^machines/(?P<machine_id>\w+)/schedules/$', 'get_schedules_for_machine'),

)