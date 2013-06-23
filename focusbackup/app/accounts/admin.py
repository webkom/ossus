# -*- coding: utf-8 -*-
from django.contrib import admin
from focusbackup.app.accounts.models import Company


class CompanyAdmin(admin.ModelAdmin):
    model = Company


admin.site.register(Company, CompanyAdmin)
