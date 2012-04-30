from django.contrib.auth import authenticate
from django.contrib.auth.models import AnonymousUser
from django.http import HttpResponse
from core.models import UserProfile

class TokenAPIAuthentication(object):
    def __init__(self, auth_func=authenticate, realm='API'):
        self.realm = realm

    def auth(self, user_pk, token):
        if token == "0":
            return None

        if len(UserProfile.objects.filter(user__pk = user_pk, api_token=token)) == 1:
            return UserProfile.objects.get(user__pk=user_pk, api_token=token)
        return None

    def is_authenticated(self, request):

        user_pk = request.POST.get("user") or request.GET.get("user")
        token = request.POST.get("token") or request.GET.get("token")

        if not user_pk or not token:
            return False

        request.user = None

        user_profile = self.auth(user_pk, token)

        if user_profile is not None:
            request.user = user_profile.user

        return not request.user in (False, None, AnonymousUser())

    def challenge(self):
        resp = HttpResponse("Authorization Required")
        resp['WWW-Authenticate'] = 'Basic realm="%s"' % self.realm
        resp.status_code = 401
        return resp