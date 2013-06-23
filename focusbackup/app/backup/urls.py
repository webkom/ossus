# -*- coding: utf-8 -*-
from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('focusbackup.app.backup.views',
                       url(r'^new/(?P<machine_id>\w+)/$', 'new', name="backups.new"),
                       url(r'^(?P<machine_id>\w+)/(?P<id>\w+)/edit/$', 'edit', name='backups.edit'),
)