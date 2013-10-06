from django import forms


class BootstrapForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super(BootstrapForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})


class BootstrapModelForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(BootstrapModelForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})
