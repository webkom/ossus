# -*- coding: utf-8 -*-
from django.forms import ModelForm
from app.backup.models import ScheduleBackup, Backup, MachineLog

class ScheduleBackupForm(ModelForm):
    class Meta:
        model = ScheduleBackup
        fields = ('name','running_backup','running_restore','current_version_in_loop')

class BackupForm(ModelForm):
    class Meta:
        model = Backup
        fields = ('time_started',)

class MachineLogForm(ModelForm):
    class Meta:
        model = MachineLog
        fields = ('datetime','text','type')