from django.conf.urls.defaults import patterns, url
from api.views.client_versions import get_client_versions

urlpatterns = patterns('api.views',

    #Machines
    (r'^machines/$', 'machines.get_machines'),
    (r'^machines/(?P<id>\w+)/$', 'machines.get_machines'),
    (r'^machines/(?P<id>\w+)/schedules/$', 'machines.get_schedules_for_machine'),
    (r'^machines/(?P<id>\w+)/settings/$', 'machines.get_settings_for_machine'),


    (r'^machines/(?P<id>\w+)/log/$', 'machines.get_log_for_machine'),
    (r'^machines/(?P<id>\w+)/create_log/$', 'machines.create_log_for_machine'),

    #Set machine version
    (r'^machines/(?P<id>\w+)/set_agent_version/(?P<version>\w+)$', 'machines.set_machine_agent_version'),
    (r'^machines/(?P<id>\w+)/set_updater_version/(?P<version>\w+)$', 'machines.set_machine_updater_version'),

    (r'^machines/(?P<id>\w+)/set_machine_external_ip/(?P<ip_address>\w+)$', 'machines.set_machine_external_ip'),

    #MachineStats
    (r'^machines/(?P<id>\w+)/create_stats/$', 'machinestats.create_stats_for_machine'),

    #Schedules
    (r'^schedules/$', 'schedules.get_schedules'),
    (r'^schedules/(?P<id>\w+)/$', 'schedules.get_schedules'),

    #Client Versions
    (r'^client_versions/$', 'client_versions.get_client_versions'),
    (r'^client_versions/current_updater/$', 'client_versions.get_current_updater'),
    (r'^client_versions/current_agent/$', 'client_versions.get_current_agent'),
    (r'^client_versions/(?P<id>\w+)/$', 'client_versions.get_client_versions'),

    #Backups
    (r'^backups/$', 'backups.get_backups'),
    (r'^backups/(?P<id>\w+)/$', 'backups.get_backups'),
    (r'^backups/(?P<id>\w+)/create_backup/$', 'backups.create_backup_for_machine'),

)