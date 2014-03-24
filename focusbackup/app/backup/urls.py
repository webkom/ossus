# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
                       url(r'^new/(?P<machine_id>\w+)/$', 'focusbackup.app.backup.views.new', name="backups.new"),
                       url(r'^(?P<machine_id>\w+)/(?P<id>\w+)/edit/$', 'focusbackup.app.backup.views.edit', name='backups.edit'),
                       url(r'^(?P<machine_id>\w+)/settings/$', 'focusbackup.api.views.machines.get_settings_for_machine'),

                       )