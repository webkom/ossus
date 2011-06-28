from app.backup.models import Machine
from piston.handler import BaseHandler
from piston.utils import rc

class MachineHandler(BaseHandler):
    model = Machine
    fields = ('id', 'machine_id', 'name', 'last_connection_to_client','is_busy','running_backup','running_restore','get_next_backup_time','get_last_backup_time', ('schedules', (
        'id', 'name', 'machine_id', 'ftp_host', 'current_day_folder_path', 'get_next_backup_time','get_last_backup_time', 'ftp_username', 'running_backup',
        'running_restore', 'ftp_password', 'ftp_folder', 'from_date', 'get_next_backup_time',
            ('folder_tasks', ('id', 'local_folder_path')), ('backups', ('id', 'time_started')))),
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