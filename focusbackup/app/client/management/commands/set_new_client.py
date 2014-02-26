# -*- coding: utf-8 -*-
from django.core.files import File

from django.core.management.commands.loaddata import Command as loaddata
from focusbackup.app.client.models import ClientVersion


class Command(loaddata):
    def handle (self, *args, **kwargs):

        client_version = ClientVersion()
        client_version.name = "New update"

        client_version.agent = File(open("/tmp/Agent.jar"))
        client_version.updater = File(open("/tmp/Updater.jar"))
        client_version.installer = File(open("/tmp/installer.jar"))

        client_version.save()
        client_version.set_current()