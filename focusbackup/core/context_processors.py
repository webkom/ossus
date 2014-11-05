# -*- coding: utf8 -*-
from django.conf import settings as _settings


def settings(request):
    return {
        'BRAND': _settings.BRAND
    }