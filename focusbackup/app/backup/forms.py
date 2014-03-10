# -*- coding: utf-8 -*-
from django import forms
from django.forms import ModelForm
from django.forms.models import inlineformset_factory
from django.forms.widgets import TextInput, Select

from focusbackup.app.backup.models import Backup, Folder, Schedule, SQL, sql_types
from focusbackup.app.machine.models import MachineLog, MachineStats
from focusbackup.core.forms import BootstrapModelForm


class BackupForm(BootstrapModelForm):
    class Meta:
        model = Backup
        fields = ('time_started', 'time_ended')


class MachineLogForm(BootstrapModelForm):
    class Meta:
        model = MachineLog
        fields = ('datetime', 'text', 'type')


class MachineStatsForm(BootstrapModelForm):
    class Meta:
        model = MachineStats
        fields = ('datetime', 'load_average', 'cpu_stolen',
                  'cpu_user', 'cpu_system', 'mem_free', 'mem_used')


class ScheduleForm(BootstrapModelForm):
    def __init__(self, *args, **kwargs):
        user = None

        if 'user' in kwargs:
            user = kwargs['user']
            del (kwargs['user'])

        super(ScheduleForm, self).__init__(*args, **kwargs)

        if user:
            self.fields['storage'].queryset = user.profile.get_storages()

    class Meta:
        model = Schedule
        fields = ("name", "storage", "from_date", 'running_backup',
                  "repeat_every_minute", "active", "versions_count")


class FolderBackupForm(BootstrapModelForm):
    local_folder_path = forms.CharField(max_length=255,
                                        widget=TextInput(attrs={'class': 'input-xxlarge'}))

    class Meta:
        model = Folder
        fields = ("local_folder_path",)


ScheduleFoldersForm = inlineformset_factory(Schedule, Folder, form=FolderBackupForm, extra=1)


class SQLBackupForm(BootstrapModelForm):
    type = forms.ChoiceField(choices=sql_types, widget=Select(attrs={'class': 'input-small', }))
    host = forms.CharField(max_length=255, widget=TextInput(attrs={'class': 'input-small', }))
    port = forms.CharField(max_length=255, widget=TextInput(attrs={'class': 'input-mini', }))
    database = forms.CharField(max_length=255, widget=TextInput(attrs={'class': 'input-small', }))
    username = forms.CharField(max_length=255, widget=TextInput(attrs={'class': 'input-small', }))
    password = forms.CharField(max_length=255, widget=TextInput(attrs={'class': 'input-small', }))

    class Meta:
        model = SQL
        fields = ("type", "host", "port", "database", "username", "password",)


ScheduleSQLsForm = inlineformset_factory(Schedule, SQL, form=SQLBackupForm, extra=1)