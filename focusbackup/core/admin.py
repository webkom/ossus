# -*- coding: utf-8 -*-
from django.contrib import admin

from focusbackup.core.models import UserProfile


# User profiles
class UserProfileAdmin(admin.ModelAdmin):
    model = UserProfile


admin.site.register(UserProfile, UserProfileAdmin)