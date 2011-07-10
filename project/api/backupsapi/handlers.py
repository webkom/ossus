from app.backup.forms import BackupForm
from app.backup.models import Backup, Machine, ScheduleBackup
from piston.handler import BaseHandler
from piston.utils import rc

class BackupHandler(BaseHandler):
    model = Backup
    fields = ('id', 'time_started', 'machine', ('schedule', (
        'id', 'current_version_in_loop', 'running_restore', 'current_day_folder_path', 'get_next_backup_time',
        'versions_count', 'running_backup', 'storage', ('folder_backups', ('id', 'local_folder_path')))))

    def read(self, request, id=None):
        all = Backup.objects.all()
        if id:
            try:
                return all.get(id=id)
            except Backup.DoesNotExist:
                return rc.NOT_FOUND
        else:
            return all


    def create(self, request, id=None):
        if id:
            instance = Backup.objects.get(id=id)
            machine = instance.machine
            schedulebackup = instance.schedule
        else:
            instance = Backup()
            machine = Machine.objects.get(id=request.POST['machine_id'])
            schedulebackup = ScheduleBackup.objects.get(id=request.POST['schedule_id'])

        machine.set_last_connection_to_client()

        form = BackupForm(request.POST, instance=instance)
        if form.is_valid():
            schedule = form.save(commit=False)
            schedule.machine = machine
            schedule.schedule = schedulebackup
            schedule.save()

            return schedule

        else:
            return form.errors