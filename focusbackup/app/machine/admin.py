# -*- coding: utf-8 -*-
from django.contrib import admin

from focusbackup.app.machine.models import Machine


class MachineAdmin(admin.ModelAdmin):
    model = Machine
    search_fields = ['id', 'name']


class MachineInline(admin.TabularInline):
    model = Machine


admin.site.register(Machine, MachineAdmin)
