# -*- coding: utf-8 -*-
from django.shortcuts import redirect
from focusbackup.app.client.models import ClientVersion


def download_current_agent(request):
    current_agent = ClientVersion.objects.get(current_agent=True)
    return redirect("/uploads/%s" % current_agent.agent.name)


def download_current_updater(request):
    current_agent = ClientVersion.objects.get(current_updater=True)
    return redirect("/uploads/%s" % current_agent.updater.name)


def download_current_setup(request):
    current_agent = ClientVersion.objects.get(current_updater=True)
    return redirect("/uploads/%s" % current_agent.installer.name)