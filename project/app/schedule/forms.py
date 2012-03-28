from django import forms
from django.db import models
from django.forms.models import ModelForm, modelformset_factory
from app.backup.models import ScheduleBackup, Storage
from django.forms.formsets import formset_factory

class ScheduleBackupForm(ModelForm):
    storage = forms.ModelChoiceField(queryset=Storage.objects.none())

    def __init__(self, *args, **kwargs):
        user = None

        if 'user' in kwargs:
            user = kwargs['user']
            del(kwargs['user'])

        super(ScheduleBackupForm, self).__init__(*args, **kwargs)

        if user:
            self.fields['storage'].queryset = user.profile.get_storages()

    class Meta:
        model = ScheduleBackup
        fields = ("name", "storage", "from_date", "repeat_every_minute", "active")