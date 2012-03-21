# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *

urlpatterns = patterns('app.accounts.views',
    (r'^login/$', 'login_view'),
    (r'^change_company/(?P<id>\w+)/$', 'change_company'),
    (r'^logout/$', 'logout_view'),
)