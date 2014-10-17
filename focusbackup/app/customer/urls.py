# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url

urlpatterns = patterns('focusbackup.app.customer.views',
                       url(r'^$', 'overview', name="customer_overview"),
                       url(r'^new/$', 'new', name="customer.new"),
                       url(r'^(?P<id>\w+)/view/$', 'view'),
                       url(r'^(?P<id>\w+)/edit/$', 'edit'),
)