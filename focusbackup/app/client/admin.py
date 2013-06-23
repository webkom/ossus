# -*- coding: utf-8 -*-
from django.contrib import admin
from focusbackup.app.client.models import ClientVersion


class ClientVersionsAdmin(admin.ModelAdmin):
    model = ClientVersion
    list_display = ['name', 'datetime', 'current_agent', 'current_updater']


admin.site.register(ClientVersion, ClientVersionsAdmin)