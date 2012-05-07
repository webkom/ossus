from api import client_versions_dict
from app.backup.forms import BackupForm
from app.backup.models import Backup, Machine, ScheduleBackup, ClientVersion
from piston.handler import BaseHandler
from piston.utils import rc

def get_current_agent():
    all = ClientVersion.objects.all()

    current_updater = all.filter(current_agent=True)

    if len(current_updater) > 0:
        return current_updater[0]

    return None

def get_current_updater():
    all = ClientVersion.objects.all()

    current_updater = all.filter(current_updater=True)

    if len(current_updater) > 0:
        return current_updater[0]

    return None

class ClientVersionHandler(BaseHandler):
    model = ClientVersion
    fields = client_versions_dict

    def read(self, request, name=None, current_agent=None, current_updater=None):
        all = ClientVersion.objects.all()
        
        if current_agent:
            return get_current_agent()

        if current_updater:
            return get_current_updater()
        
        if name:
            try:
                return all.get(name=name)
            except ClientVersion.DoesNotExist:
                return rc.NOT_FOUND
        else:
            return all
