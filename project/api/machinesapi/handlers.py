from app.backup.forms import MachineLogForm, MachineStatsForm
from app.backup.models import Machine, MachineLog, MachineStats
from piston.handler import BaseHandler
from piston.utils import rc

class MachineHandler(BaseHandler):
    model = Machine
    fields = ('id', 'machine_id', 'name', 'ip','last_connection_to_client','is_busy','running_backup','running_restore','get_next_backup_time','get_last_backup_time', ('updatelogs',('id','type','datetime')),('schedules', (
        'id', 'name', 'machine_id', 'storage','current_day_folder_path','current_version_in_loop', 'versions_count','get_next_backup_time','get_last_backup_time', 'running_backup',
        'running_restore', 'from_date', 'get_next_backup_time',
            ('folder_backups', ('id', 'local_folder_path')), ('sql_backups', ('id', 'type','host','port','database','username','password')), ('backups', ('id', 'time_started')))),
                  ('backups', ('id', 'time_started','day_folder_path','is_recoverable',('schedule',('id','name',)))), )

    def read(self, request, offset=0, limit=None, id=None):
        
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

class MachineStatsHandler(BaseHandler):
    model = MachineStats
    fields = ('id', ('machine',('id','name')), 'datetime','load_average','cpu_system','cpu_stolen','cpu_user','mem_free','mem_used')

    def read(self, request, offset=0, limit=None, machine_id=None):
        all = self.model.objects.all().order_by('-id')

        if machine_id:
            try:
                all =  all.filter(machine__machine_id=machine_id)
            except self.model.DoesNotExist:
                return rc.NOT_FOUND

        if limit:
            all = all[offset:limit]

        return all

    def create(self, request, id=None):
        instance = self.model()
        machine = Machine.objects.get(machine_id = (request.POST['machine_id']))

        machine.set_last_connection_to_client()

        form = MachineStatsForm(request.POST, instance=instance)
        if form.is_valid():
            log = form.save(commit=False)
            log.machine = machine
            log.save()
            return log
        else:
            print form.errors
            return form.errors


class MachineLogHandler(BaseHandler):
    model = MachineLog
    fields = ('id', ('machine',('id','name')), 'datetime','text','type',)

    def read(self, request, offset=0, limit=None, machine_id=None):
        all = MachineLog.objects.all().order_by('-id')

        if machine_id:
            try:
                all =  all.filter(machine__machine_id=machine_id)
            except MachineLog.DoesNotExist:
                return rc.NOT_FOUND

        if limit:
            all = all[offset:limit]

        return all

    def create(self, request, id=None):
        instance = MachineLog()
        machine = Machine.objects.get(machine_id = (request.POST['machine_id']))

        machine.set_last_connection_to_client()

        form = MachineLogForm(request.POST, instance=instance)
        if form.is_valid():
            log = form.save(commit=False)
            log.machine = machine
            log.save()
            return log
        else:
            print form.errors
            return form.errors