# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url

urlpatterns = patterns('focusbackup.app.machine.views',
                       url(r'^$', 'overview', name="machine_overview"),
                       url(r'^new/$', 'new', name="machines.new"),
                       url(r'^(?P<id>\w+)/view/$', 'view', name="machines.view"),
                       url(r'^(?P<id>\w+)/view/log/$', 'view_log', name="machines.view_log"),
                       url(r'^(?P<id>\w+)/view/schedules/$', 'view_schedules', name="machines.view_schedules"),
                       url(r'^(?P<id>\w+)/view/backups/$', 'view_backups', name="machines.view_backups"),
                       url(r'^(?P<id>\w+)/edit/$', 'edit'),

                       url(r'^templates/$', 'templates', name="templates.overview"),
                       url(r'^(?P<id>\w+)/template/view/$', 'view_template', name="templates.view"),
                       url(r'^(?P<id>\w+)/template/view/schedules/$', 'view_template_schedules',
                           name="templates.view_schedules"),

)