# -*- coding: utf-8 -*-

from django.contrib import admin

from focusbackup.app.backup.models import Backup, Schedule, Folder, SQL

admin.site.register(Backup)
admin.site.register(Schedule)
admin.site.register(Folder)
admin.site.register(SQL)