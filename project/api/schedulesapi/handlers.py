from app.backup.forms import ScheduleBackupForm
from app.backup.models import Machine, ScheduleBackup
from piston.handler import BaseHandler
from piston.utils import rc

class SchedulesBackupHandler(BaseHandler):
    model = ScheduleBackup
    fields = (
        'id', 'name', 'ftp_host', 'machine_id', 'running_backup', 'running_restore','ftp_username', 'ftp_password', 'ftp_folder', 'from_date', 'get_next_backup_time',
            ('folder_tasks', ('id', 'local_folder_path')),('backups', ('id', 'time_started')))

    def read(self, request, id=None):
        all = ScheduleBackup.objects.all()
        if id:
            try:
                return all.get(id=id)
            except ScheduleBackup.DoesNotExist:
                return rc.NOT_FOUND
        else:
            return all


    def create(self, request, id=None):
        if id:
            instance = ScheduleBackup.objects.get(id=id)
        else:
            instance = ScheduleBackup()

        form = ScheduleBackupForm(request.POST, instance=instance)

        if form.is_valid():
            schedule = form.save(commit=False)
            schedule.owner = request.user
            schedule.save()

            return schedule

        else:
            return form.errors