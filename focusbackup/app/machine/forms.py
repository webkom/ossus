from django.forms.models import ModelForm
from focusbackup.app.backup.models import Machine

class MachineForm(ModelForm):
    def __init__(self, *args, **kwargs):
        user = None
        if 'user' in kwargs:
            user = kwargs['user']
            del(kwargs['user'])

        super(MachineForm, self).__init__(*args, **kwargs)

        if user:
            self.fields['customer'].queryset = user.profile.get_customers()

    class Meta:
        model = Machine
        fields = (
        'id', 'name', 'customer', 'local_temp_folder', 'agent_folder', 'mysql_dump', 'auto_version', 'run_install', 'selected_agent_version', 'selected_updater_version')