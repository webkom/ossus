from django.forms.models import ModelForm
from focusbackup.app.backup.models import MachineStats

class MachineStatsForm(ModelForm):
    class Meta:
        model = MachineStats
        fields = ('datetime', 'load_average', 'cpu_stolen', 'cpu_user', 'cpu_system', 'mem_free', 'mem_used')