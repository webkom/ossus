from django.forms.models import ModelForm
from app.backup.models import Machine

class MachineForm(ModelForm):
    class Meta:
        model = Machine
        fields = ('name','location','ip',)