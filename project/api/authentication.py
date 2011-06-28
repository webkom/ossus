from django.http import HttpResponse

class BackupBasicAPIAuthentication(object):
    def __init__(self):
        self.realm = "FNCIT BACKUP API"

    def is_authenticated(self, request):
        return True

    def challenge(self):
        resp = HttpResponse("Authorization Required")
        resp['WWW-Authenticate'] = 'Basic realm="%s"' % self.realm
        resp.status_code = 401
        return resp