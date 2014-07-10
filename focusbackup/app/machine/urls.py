# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url

urlpatterns = patterns('focusbackup.app.machine.views',
                       url(r'^$', 'overview', name="machine_overview"),
                       url(r'^new/$', 'new', name="machines.new"),
                       url(r'^install-instructions/$', 'install_instructions', name="machines.install_instructions"),
                       url(r'^install-instructions-linux/$', 'install_instructions_linux', name="machines.install_instructions_linux"),
                       url(r'^(?P<id>\w+)/view/$', 'view', name="machines.view"),
                       url(r'^(?P<id>\w+)/view/log/$', 'view_log', name="machines.view_log"),
                       url(r'^(?P<id>\w+)/view/schedules/$', 'view_schedules', name="machines.view_schedules"),
                       url(r'^(?P<id>\w+)/view/backups/$', 'view_backups', name="machines.view_backups"),
                       url(r'^(?P<id>\w+)/edit/$', 'edit'),
                       url(r'^(?P<id>\w+)/settings/$', 'settings'),
                       url(r'^(?P<id>\w+)/toggle_busy/$', 'toggle_busy', name="machines.toggle_busy"),
                       url(r'^(?P<id>\w+)/stop_schedule/(?P<schedule_id>\w+)/$', 'stop_schedule', name="machines.stop_schedule"),
                       url(r'^(?P<id>\w+)/toggle_active/$', 'toggle_active', name="machines.toggle_active"),
                       url(r'^(?P<id>\w+)/delete/$', 'delete'),
                       url(r'^(?P<id>\w+)/replace-schedules/(?P<template_id>\w+)/$', 'replace_schedules_with_template'),

                       url(r'^templates/$', 'templates', name="templates.overview"),
                       url(r'^(?P<id>\w+)/template/view/$', 'view_template', name="templates.view"),
                       url(r'^(?P<id>\w+)/template/view/schedules/$', 'view_template_schedules',
                           name="templates.view_schedules"),
)
