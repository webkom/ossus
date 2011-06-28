from app.backup.forms import ScheduleBackupForm
from app.backup.models import ScheduleBackup, Company
from piston.handler import BaseHandler
from piston.utils import rc

class CompanyHandler(BaseHandler):
    model = Company
    fields = ("id", "name", ('customers', ('id', 'name', ('locations', (
        'id', 'name', ('machines', (
            'id', 'name', 'machine_id', 'running_restore','running_backup','is_busy',
                ('schedules', ('id', 'name', ('backups', ('id', 'time_started', 'day_folder_path')))))))))))

    def read(self, request, id=None):
        print request.user.companies.all()
        all = Company.objects.all()
        if id:
            try:
                return all.get(id=id)
            except Company.DoesNotExist:
                return rc.NOT_FOUND
        else:
            return all