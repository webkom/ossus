# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *

urlpatterns = patterns('app.accounts.views',
        (r'^login/$', 'login_view'),
        (r'^logout/$', 'logout_view'),
                       )