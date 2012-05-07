from api import machine_dict, schedule_dict, backup_dict
from app.backup.forms import MachineLogForm, MachineStatsForm
from app.backup.models import Machine, MachineLog, MachineStats, ClientVersion
from piston.handler import BaseHandler
from piston.utils import rc

class MachineHandler(BaseHandler):
    model = Machine
    fields = machine_dict + (
    ('updatelogs', ('id', 'type', 'datetime')), ('backups', backup_dict), )

    def read(self, request, offset=0, limit=None, id=None, agent_version_id=False, updater_version_id=False):
        all = request.user.profile.get_machines()

        if id:

            try:
                machine = all.get(machine_id=id)

                if agent_version_id:
                    machine.current_agent_version = ClientVersion.objects.get(id=agent_version_id)

                elif updater_version_id:
                    machine.current_updater_version = ClientVersion.objects.get(id=updater_version_id)

                machine.save()

                return machine

            except Machine.DoesNotExist:
                return rc.NOT_FOUND
        else:
            return all

    def create(self, request, id=False):
        pass

class MachineStatsHandler(BaseHandler):
    model = MachineStats
    fields = (
    'id', ('machine', ('id', 'name')), 'datetime', 'load_average', 'cpu_system', 'cpu_stolen', 'cpu_user', 'mem_free',
    'mem_used')

    def read(self, request, offset=0, limit=None, machine_id=None):
        all = self.model.objects.all().order_by('-id')

        if machine_id:
            try:
                all = all.filter(machine__machine_id=machine_id)
            except self.model.DoesNotExist:
                return rc.NOT_FOUND

        if limit:
            all = all[offset:limit]

        return all

    def create(self, request, id=None):
        instance = self.model()
        machine = Machine.objects.get(machine_id=(request.POST['machine_id']))

        machine.set_last_connection_to_client()

        form = MachineStatsForm(request.POST, instance=instance)
        if form.is_valid():
            log = form.save(commit=False)
            log.machine = machine
            log.save()
            return log
        else:
            return form.errors


class MachineLogHandler(BaseHandler):
    model = MachineLog
    fields = ('id', ('machine', ('id', 'name')), 'datetime', 'text', 'type',)

    def read(self, request, offset=0, limit=None, machine_id=None):
        all = MachineLog.objects.all().order_by('-id')

        if machine_id:
            try:
                all = all.filter(machine__machine_id=machine_id)
            except MachineLog.DoesNotExist:
                return rc.NOT_FOUND

        if limit:
            all = all[offset:limit]

        return all

    def create(self, request, id=None):
        instance = MachineLog()
        machine = Machine.objects.get(machine_id=(request.POST['machine_id']))

        machine.set_last_connection_to_client()

        form = MachineLogForm(request.POST, instance=instance)
        if form.is_valid():
            log = form.save(commit=False)
            log.machine = machine
            log.save()
            return log
        else:
            return form.errors