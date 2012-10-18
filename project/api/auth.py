# -*- coding: utf-8 -*-
import functools, inspect, copy
from api.models import Token
from django.http import Http404, HttpResponse
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

class require_valid_api_token:
    api_token = None
    api_user = None

    def __call__(self, func):

        def validate_api_token(request, *args, **kwargs):

            #if settings.DEBUG and request.user.id:
            #    return func(request, *args, **kwargs)

            if 'api_token' in request.POST and 'api_user' in request.POST:
                api_token = request.POST['api_token']
                api_user = request.POST['api_user']

                if Token.objects.filter(api_token=api_token, api_user=api_user).count() == 1:
                    request.user = User.objects.get(id=api_user)

                    return func(request, *args, **kwargs)

            elif 'api_token' in request.GET and 'api_user' in request.GET:
                api_token = request.GET['api_token']
                api_user = request.GET['api_user']

                if Token.objects.filter(api_token=api_token, api_user=api_user).count() == 1:
                    request.user = User.objects.get(id=api_user)

                    return func(request, *args, **kwargs)

            elif 'username' in request.GET and 'password' in request.GET:
                username = request.GET['username']
                password = request.GET['password']

                user = authenticate(username=username, password=password)

                if user is not None:
                    login(request, user)
                    return func(request, *args, **kwargs)

            resp = HttpResponse()
            resp.status_code = 403
            return resp

        functools.update_wrapper(validate_api_token, func)

        return validate_api_token

