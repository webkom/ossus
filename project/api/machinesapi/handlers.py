from app.backup.forms import MachineLogForm
from app.backup.models import Machine, MachineLog
from piston.handler import BaseHandler
from piston.utils import rc

class MachineHandler(BaseHandler):
    model = Machine
    fields = ('id', 'machine_id', 'name', 'ip','last_connection_to_client','is_busy','running_backup','running_restore','get_next_backup_time','get_last_backup_time', ('schedules', (
        'id', 'name', 'machine_id', 'storage','current_day_folder_path','current_version_in_loop', 'versions_count','get_next_backup_time','get_last_backup_time', 'running_backup',
        'running_restore', 'from_date', 'get_next_backup_time',
            ('folder_backups', ('id', 'local_folder_path')), ('backups', ('id', 'time_started')))),
                  ('backups', ('id', 'time_started','day_folder_path')), )

    def read(self, request, id=None):
        all = Machine.objects.all()
        if id:
            try:
                return all.get(machine_id=id)
            except Machine.DoesNotExist:
                return rc.NOT_FOUND
        else:
            return all

    def create(self, request, id=False):
        pass


class MachineLogHandler(BaseHandler):
    model = MachineLog
    fields = ('id', 'machine', 'datetime','text','type',)

    def read(self, request, id=None):
        all = MachineLog.objects.all()
        if id:
            try:
                return all.get(machine_id=id)
            except MachineLog.DoesNotExist:
                return rc.NOT_FOUND
        else:
            return all

    def create(self, request, id=None):

        instance = MachineLog()
        machine = Machine.objects.get(id = request.POST['machine_id'])

        machine.set_last_connection_to_client()

        form = MachineLogForm(request.POST, instance=instance)
        if form.is_valid():
            log = form.save(commit=False)
            log.machine = machine
            log.save()

            return log

        else:
            return form.errors