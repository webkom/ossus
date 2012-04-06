from django import forms
from django.db import models
from django.forms.models import ModelForm, modelformset_factory, inlineformset_factory
from app.backup.models import ScheduleBackup, Storage, FolderBackup, SQLBackup
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


class FolderBackupForm(ModelForm):
    local_folder_path = forms.CharField(max_length=255)

    def __init__(self, *args, **kwargs):
        super(FolderBackupForm, self).__init__(*args, **kwargs)

    class Meta:
        model = FolderBackup
        fields = ("local_folder_path",)

ScheduleFoldersForm = inlineformset_factory(ScheduleBackup, FolderBackup, form=FolderBackupForm,  extra=3)


class SQLBackupForm(ModelForm):

    class Meta:
        model = SQLBackup
        fields = ("type","host","port","database", "username","password",)

ScheduleSQLsForm = inlineformset_factory(ScheduleBackup, SQLBackup, form=SQLBackupForm,  extra=1)


