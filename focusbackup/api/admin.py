# -*- coding: utf-8 -*-

from focusbackup.api.models import Token
from django.contrib import admin


class TokenAdmin(admin.ModelAdmin):
    model = Token


admin.site.register(Token, TokenAdmin)