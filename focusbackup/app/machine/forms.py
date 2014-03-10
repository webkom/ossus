# -*- coding: utf-8 -*-
from django.forms.models import ModelForm
from focusbackup.app.backup.models import Machine
from focusbackup.core.forms import BootstrapModelForm


class MachineForm(BootstrapModelForm):
    def __init__(self, *args, **kwargs):
        user = None
        if 'user' in kwargs:
            user = kwargs['user']
            del (kwargs['user'])

        super(MachineForm, self).__init__(*args, **kwargs)

        if user:
            self.fields['customer'].queryset = user.profile.get_customers()

    class Meta:
        model = Machine
        fields = ('id', 'name', 'customer', 'local_temp_folder', 'agent_folder', 'template')
