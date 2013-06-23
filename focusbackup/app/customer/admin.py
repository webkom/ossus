# -*- coding: utf-8 -*-
from django.contrib import admin
from focusbackup.app.customer.models import Customer
from focusbackup.app.machine.admin import MachineInline


class CustomerAdmin(admin.ModelAdmin):
    model = Customer
    inlines = [
        MachineInline,
    ]

admin.site.register(Customer, CustomerAdmin)