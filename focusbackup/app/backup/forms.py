# -*- coding: utf-8 -*-
from django.forms import ModelForm
from focusbackup.app.backup.models import ScheduleBackup, Backup, MachineLog, MachineStats

class ScheduleBackupForm(ModelForm):
    class Meta:
        model = ScheduleBackup
        fields = ('name', 'running_backup', 'running_restore', 'current_version_in_loop')


class BackupForm(ModelForm):
    class Meta:
        model = Backup
        fields = ('time_started', 'time_ended')


class MachineLogForm(ModelForm):
    class Meta:
        model = MachineLog
        fields = ('datetime', 'text', 'type')


class MachineStatsForm(ModelForm):
    class Meta:
        model = MachineStats
        fields = ('datetime', 'load_average', 'cpu_stolen', 'cpu_user', 'cpu_system', 'mem_free', 'mem_used')

