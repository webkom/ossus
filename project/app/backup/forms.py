# -*- coding: utf-8 -*-
from django.forms import ModelForm
from app.backup.models import ScheduleBackup, Backup

class ScheduleBackupForm(ModelForm):
    class Meta:
        model = ScheduleBackup
        fields = ('name','running_backup','running_restore',)

class BackupForm(ModelForm):
    class Meta:
        model = Backup
        fields = ('time_started',)