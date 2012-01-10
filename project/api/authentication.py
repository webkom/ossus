from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login

class BackupBasicAPIAuthentication(object):
    def __init__(self):
        self.realm = "FOCUS24 API"

    def is_authenticated(self, request):
        auth_string = request.META.get('HTTP_AUTHORIZATION', None)

        if not auth_string:
            return False

        (authmeth, auth) = auth_string.split(" ", 1)

        if not authmeth.lower() == 'basic':
            return False

        auth = auth.strip().decode('base64')
        (username, password) = auth.split(':', 1)

        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)

                return True

        return False

    def challenge(self):
        resp = HttpResponse("Authorization Required")
        resp['WWW-Authenticate'] = 'Basic realm="%s"' % self.realm
        resp.status_code = 401
        return resp