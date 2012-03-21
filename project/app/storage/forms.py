from django.forms.models import ModelForm
from app.backup.models import Storage

class StorageForm(ModelForm):
    class Meta:
        model = Storage
        fields = ('type','host','username','password','folder')