from django import forms

class BackupAPIForm(forms.Form):
    schedule_id = forms.CharField()
    time_started = forms.CharField()
    time_ended = forms.CharField()

