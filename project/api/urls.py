from django.conf.urls.defaults import patterns, url
from api.views.client_versions import get_client_versions

urlpatterns = patterns('api.views',

    #Machines

    (r'^machines/$', 'machines.get_machines'),
    (r'^machines/(?P<machine_id>\w+)/$', 'machines.get_machines'),
    (r'^machines/(?P<machine_id>\w+)/schedules/$', 'machines.get_schedules_for_machine'),

    (r'^machines/(?P<machine_id>\w+)/log/$', 'machines.get_log_for_machine'),
    (r'^machines/(?P<machine_id>\w+)/create_log/$', 'machines.create_log_for_machine'),

    #Schedules
    (r'^schedules/$', 'schedules.get_schedules'),
    (r'^schedules/(?P<id>\w+)/$', 'schedules.get_schedules'),

    #Client Versions
    (r'^client_versions/$', 'client_versions.get_client_versions'),
    (r'^client_versions/current_updater/$', 'client_versions.get_current_updater'),
    (r'^client_versions/current_agent/$', 'client_versions.get_current_agent'),
    (r'^client_versions/(?P<id>\w+)/$', 'client_versions.get_client_versions'),

)