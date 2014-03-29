# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url

urlpatterns = patterns('focusbackup.api.views',

                       #Machines
                       (r'^machines/$', 'machines.get_machines'),
                       (r'^machines/(?P<id>\w+)/$', 'machines.get_machines'),
                       (r'^machines/(?P<id>\w+)/schedules/$', 'machines.get_schedules_for_machine'),
                       (r'^machines/(?P<id>\w+)/settings/$', 'machines.get_settings_for_machine'),
                       (r'^machines/(?P<id>\w+)/log/$', 'machines.get_log_for_machine'),
                       (r'^machines/(?P<id>\w+)/deactivate/$', 'machines.deactivate'),
                       (r'^machines/(?P<id>\w+)/create_log/$', 'machines.create_log_for_machine'),
                       (r'^machines/(?P<id>\w+)/clone/(?P<name>[\w+. -]*)/$', 'machines.create_new_machine_from_template'),

                       #Set machine version
                       (r'^machines/(?P<id>\w+)/set_agent_version/(?P<version>\w+)$',
                        'machines.set_machine_agent_version'),
                       (r'^machines/(?P<id>\w+)/set_updater_version/(?P<version>\w+)$',
                        'machines.set_machine_updater_version'),

                       (r'^machines/(?P<id>\w+)/set_machine_external_ip/(?P<ip_address>[0-9\.]*)$',
                        'machines.set_machine_external_ip'),

                       (r'^machines/(?P<id>\w+)/set_busy_updating/(?P<busy>\d)/$', 'machines.set_busy_updating'),

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


                       #Get external IP
                       (r'^ip/$', 'common.get_external_ip'),

)