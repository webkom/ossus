import json
from django.views.decorators.csrf import csrf_exempt
from api.auth import require_valid_api_token
from api.views.common import render_data, HandleQuerySets
from api.views.helpers import build_client_version
from app.backup.models import ClientVersion

@require_valid_api_token()
def get_client_versions(request, id=False):
    if id:
        return render_data("client_version", build_client_version(ClientVersion.objects.get(id=id)))

    else:
        send_object = []
        for obj in ClientVersion.objects.all():
            send_object.append(build_client_version(obj))

        return render_data("client_versions", send_object)

@require_valid_api_token()
def get_current_updater(request):
    return render_data("client_version", build_client_version(ClientVersion.objects.get(current_updater=True)))

@require_valid_api_token()
def get_current_agent(request):
    return render_data("client_version", build_client_version(ClientVersion.objects.get(current_agent=True)))