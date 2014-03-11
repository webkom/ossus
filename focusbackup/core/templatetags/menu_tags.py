# -*- coding: utf-8 -*-
from django.template import Library

register = Library()


@register.simple_tag
def active(request, pattern):
    import re

    print request.path
    if re.search(pattern, request.path):
        return "active"
    return ""