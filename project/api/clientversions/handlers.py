from app.backup.forms import BackupForm
from app.backup.models import Backup, Machine, ScheduleBackup, ClientVersion
from piston.handler import BaseHandler
from piston.utils import rc

class ClientVersionHandler(BaseHandler):
    model = ClientVersion
    fields = ('')

    def read(self, request, id=None):
        all = ClientVersion.objects.all()
        if id:
            try:
                return all.get(id=id)
            except ClientVersion.DoesNotExist:
                return rc.NOT_FOUND
        else:
            return all