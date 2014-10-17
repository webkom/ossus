# -*- coding: utf-8 -*-
from focusbackup.app.backup.models import Storage
from focusbackup.core.forms import BootstrapModelForm


class StorageForm(BootstrapModelForm):
    class Meta:
        model = Storage
        fields = ('type', 'name', 'host', 'username', 'password', 'folder', 'notes')