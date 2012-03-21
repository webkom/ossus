# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *

urlpatterns = patterns('app.accounts.views',
    (r'^login/$', 'login_view'),
    url(r'^change_company/(?P<id>\w+)/$', 'change_company', name="change_company"),
    (r'^logout/$', 'logout_view'),
)