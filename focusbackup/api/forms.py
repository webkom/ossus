# -*- coding: utf-8 -*-
from django import forms
from django.forms.models import ModelForm
from focusbackup.app.machine.models import MachineStats


class BackupAPIForm(forms.Form):
    schedule_id = forms.CharField()
    time_started = forms.CharField()
    time_ended = forms.CharField()


class LogAPIForm(forms.Form):
    id = forms.CharField()
    type = forms.CharField()
    text = forms.CharField()


class ScheduleAPIForm(forms.Form):
    name = forms.CharField()
    running_backup = forms.CharField()
    running_restore = forms.CharField()
    current_version_in_loop = forms.CharField()


class MachineStatsForm(ModelForm):
    class Meta:
        model = MachineStats
        fields = ('datetime', 'load_average', 'cpu_stolen', 'cpu_user', 'cpu_system', 'mem_free', 'mem_used')