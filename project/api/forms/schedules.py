from django import forms

class ScheduleAPIForm(forms.Form):
    name = forms.CharField()
    running_backup = forms.CharField()
    running_restore = forms.CharField()
    current_version_in_loop = forms.CharField()