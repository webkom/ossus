# -*- coding: utf-8 -*-
from django.forms.models import ModelForm
from focusbackup.app.customer.models import Customer
from focusbackup.core.forms import BootstrapModelForm


class CustomerForm(BootstrapModelForm):
    class Meta:
        model = Customer
        fields = ('name', 'address', 'contact_person', 'contact_phone', 'contact_email')