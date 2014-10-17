# -*- coding: utf-8 -*-
from focusbackup.api.auth import RequireValidToken
from focusbackup.api.views.common import render_data
from focusbackup.api.views.helpers import build_client_version
from focusbackup.app.client.models import ClientVersion


@RequireValidToken()
def get_client_versions(request, id=False):
    if id:
        return render_data("client_version", build_client_version(ClientVersion.objects.get(id=id)))

    else:
        send_object = []
        for obj in ClientVersion.objects.all():
            send_object.append(build_client_version(obj))

        return render_data("client_versions", send_object)


@RequireValidToken()
def get_current_updater(request):
    return render_data("client_version",
                       build_client_version(ClientVersion.objects.get(current_updater=True)))


@RequireValidToken()
def get_current_agent(request):
    return render_data("client_version",
                       build_client_version(ClientVersion.objects.get(current_agent=True)))
