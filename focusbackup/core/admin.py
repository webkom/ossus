# -*- coding: utf-8 -*-
from focusbackup.core.models import UserProfile
from django.contrib import admin


#User profiles
class UserProfileAdmin(admin.ModelAdmin):
    model = UserProfile


admin.site.register(UserProfile, UserProfileAdmin)