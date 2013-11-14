# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url

urlpatterns = patterns('focusbackup.app.storage.views',
    url(r'^$', 'overview', name="storage_overview"),
    (r'^new/$', 'new'),
    (r'^(?P<id>\w+)/view/$', 'edit'),
    (r'^(?P<id>\w+)/edit/$', 'edit'),
)