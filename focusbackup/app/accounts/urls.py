# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url

urlpatterns = patterns('focusbackup.app.accounts.views',
    (r'^login/$', 'login_view'),
    url(r'^change_company/(?P<id>\w+)/$', 'change_company', name="change_company"),
    url(r'^logout/$', 'logout_view', name="logout"),
)