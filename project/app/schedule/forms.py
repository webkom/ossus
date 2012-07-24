from django import forms
from django.forms.models import ModelForm, modelformset_factory, inlineformset_factory
from django.forms.widgets import TextInput, Select
from app.backup.models import ScheduleBackup, Storage, FolderBackup, SQLBackup, sql_types

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
        fields = ("name", "storage", "from_date", "repeat_every_minute", "active", "running_backup", "running_restore")

class FolderBackupForm(ModelForm):
    local_folder_path = forms.CharField(max_length=255, widget=TextInput(attrs={'class': 'input-small'}))

    class Meta:
        model = FolderBackup
        fields = ("local_folder_path",)

ScheduleFoldersForm = inlineformset_factory(ScheduleBackup, FolderBackup, form=FolderBackupForm, extra=1)

class SQLBackupForm(ModelForm):
    type = forms.ChoiceField(choices=sql_types, widget=Select(attrs={'class': 'input-small', }))
    host = forms.CharField(max_length=255, widget=TextInput(attrs={'class': 'input-small', }))
    port = forms.CharField(max_length=255, widget=TextInput(attrs={'class': 'input-mini', }))
    database = forms.CharField(max_length=255, widget=TextInput(attrs={'class': 'input-small', }))
    username = forms.CharField(max_length=255, widget=TextInput(attrs={'class': 'input-small', }))
    password = forms.CharField(max_length=255, widget=TextInput(attrs={'class': 'input-small', }))

    class Meta:
        model = SQLBackup
        fields = ("type", "host", "port", "database", "username", "password",)

ScheduleSQLsForm = inlineformset_factory(ScheduleBackup, SQLBackup, form=SQLBackupForm, extra=1)
