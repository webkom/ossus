from django import forms

class LogAPIForm(forms.Form):
    id = forms.CharField()
    type = forms.CharField()
    text = forms.CharField()