# -*- coding: utf-8 -*-
from django.shortcuts import redirect
from focusbackup.app.client.models import ClientVersion


def download_current_agent(request):
    current = ClientVersion.objects.get(current_agent=True)
    return redirect("/uploads/%s" % current.agent.name)


def download_current_updater(request):
    current = ClientVersion.objects.get(current_updater=True)
    return redirect("/uploads/%s" % current.updater.name)


def download_current_installer(request):
    current = ClientVersion.objects.get(current_installer=True)
    return redirect("/uploads/%s" % current.installer.name)
