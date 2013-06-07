from django.forms.models import ModelForm
from focusbackup.app.backup.models import Storage

class StorageForm(ModelForm):
    class Meta:
        model = Storage
        fields = ('type','name','host','username','password','folder','notes')