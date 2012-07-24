import json
from django.views.decorators.csrf import csrf_exempt
from api.auth import require_valid_api_token
from api.views.common import render_data, HandleQuerySets
from api.views.helpers import build_schedule_fields, build_machine_fields, build_machine_log, build_backup_fields
from app.backup.models import Machine, Backup

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
    return render_data("hei", {'a': 'b'})

create_backup_for_machine = csrf_exempt(create_backup_for_machine)
