from django import forms

class LogAPIForm(forms.Form):
    machine_id = forms.CharField()
    type = forms.CharField()
    text = forms.CharField()