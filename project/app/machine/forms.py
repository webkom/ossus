from django.forms.models import ModelForm
from app.backup.models import Machine

class MachineForm(ModelForm):
    class Meta:
        model = Machine
        fields = ('machine_id','name','customer','auto_version', 'selected_agent_version','selected_updater_version')