from django.forms.models import ModelForm
from app.backup.models import Machine

class CustomerForm(ModelForm):
    class Meta:
        model = Machine
        fields = ('name',)