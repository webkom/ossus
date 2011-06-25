# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *
import os
from django.conf import settings

urlpatterns = patterns('',
                      )

if settings.DEBUG:
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns
    urlpatterns += staticfiles_urlpatterns()