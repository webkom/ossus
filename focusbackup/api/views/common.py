# -*- coding: utf-8 -*-
import json
import datetime

from django.http import HttpResponse
from django.utils import simplejson
from django.db.models.query import QuerySet
from django.core import serializers
from focusbackup.api.models import Token


class HandleQuerySets(simplejson.JSONEncoder):
    """ simplejson.JSONEncoder extension: handle querysets """

    def default(self, obj):
        if isinstance(obj, QuerySet):
            return serializers.serialize("python", obj, ensure_ascii=False)
        elif isinstance(obj, datetime.datetime):
            return obj.strftime("%Y-%m-%dT%H:%M:%S")


def render_data(name, data):
    """
    Returns a httpResponse with json where name is the outer scope and data is a python array with objects as dicts
    """

    output_data = {name: data}

    if not name:
        output_data = data

    s = json.dumps(output_data, cls=HandleQuerySets, indent=4)
    return HttpResponse(s, mimetype="application/json")


def get_external_ip(request):
    ip_address = request.META.get('HTTP_X_FORWARDED_FOR', ) or request.META.get('REMOTE_ADDR')
    return HttpResponse(ip_address)


def check_token(token):
    """
    Checks if there exists a token and it is active
    """

    find_token = Token.objects.filter(token=token, active=True)
    return len(find_token) > 0


class APIStatus:
    unknown_error = {'id': '0', 'message': 'Unknown error'}
    success = {'id': '1', 'message': 'Success'}
    invalid_token = {'id': '2', 'message': 'Invalid token'}


def APIStatusResponse(error=APIStatus.unknown_error):
    """
    Returns a error message in JSON
    """
    output_data = {'status_code': error['id'], 'status_message': error['message']}
    s = json.dumps(output_data, cls=HandleQuerySets, indent=4)
    return HttpResponse(s, mimetype="application/json")