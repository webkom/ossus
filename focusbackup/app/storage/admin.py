# -*- coding: utf-8 -*-

from django.contrib import admin
from focusbackup.app.storage.models import Storage


class StorageAdmin(admin.ModelAdmin):
    model = Storage


admin.site.register(Storage, StorageAdmin)
