import json
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from api.auth import require_valid_api_token
from api.forms.backups import BackupAPIForm
from api.views.common import render_data, HandleQuerySets
from api.views.helpers import build_schedule_fields, build_machine_fields, build_machine_log, build_backup_fields
from app.backup.models import Machine, Backup, ScheduleBackup

@require_valid_api_token()
def get_backups(request, id=False):
    if id:
        return render_data("backups", build_backup_fields(Backup.objects.get(id=id)))

    else:
        send_object = []
        for obj in Backup.objects.all():
            send_object.append(build_backup_fields(obj))

        return render_data("backups", send_object)

get_backups = csrf_exempt(get_backups)


@require_valid_api_token()
def create_backup_for_machine(request, machine_id):

    if machine_id:
        machine = Machine.objects.get(machine_id=machine_id)

        if request.method == "POST":
            form = BackupAPIForm(request.POST)

            if form.is_valid():
                backup = Backup()

                print request.POST['time_started']

                backup.machine = machine
                backup.schedule = ScheduleBackup.objects.get(id=request.POST['schedule_id'])
                backup.time_started = request.POST['time_started']
                backup.time_ended = request.POST['time_ended']

                backup.save()


                return render_data("backup", build_backup_fields(backup))

    return HttpResponse("ERROR")

create_backup_for_machine = csrf_exempt(create_backup_for_machine)