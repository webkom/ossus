from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from focusbackup.api.auth import RequireValidToken
from focusbackup.api.views.common import render_data
from focusbackup.api.views.helpers import build_backup_fields
from focusbackup.app.backup.models import Machine, Backup, Schedule
from focusbackup.api.forms import BackupAPIForm


@RequireValidToken()
def get_backups(request, id=False):
    if id:
        return render_data("backups", build_backup_fields(Backup.objects.get(id=id)))

    else:
        send_object = []
        for obj in Backup.objects.all():
            send_object.append(build_backup_fields(obj))

        return render_data("backups", send_object)


get_backups = csrf_exempt(get_backups)


@RequireValidToken()
def create_backup_for_machine(request, id):
    if id:
        machine = Machine.objects.get(id=id)

        if request.method == "POST":
            form = BackupAPIForm(request.POST)

            if form.is_valid():
                backup = Backup()
                schedule = Schedule.objects.get(id=request.POST['schedule_id'])

                backup.machine = machine
                backup.schedule = schedule
                backup.time_started = request.POST['time_started']
                backup.time_ended = request.POST['time_ended']

                if 'upload_path' in request.POST:
                    backup.day_folder_path = request.POST['upload_path']

                if 'file_name' in request.POST:
                    backup.file_name = request.POST['file_name']

                backup.save()

                return render_data("backup", build_backup_fields(backup))

    return HttpResponse("ERROR")


create_backup_for_machine = csrf_exempt(create_backup_for_machine)
