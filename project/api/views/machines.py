import json
from api.auth import require_valid_api_token
from api.views.common import render_data, HandleQuerySets
from app.backup.models import Machine

@require_valid_api_token()
def get_machines(request, machine_id=False):
    def build_event_fields(machine):
        current_av = machine.current_agent_version
        current_uv = machine.current_updater_version

        print current_av.updater_link

        machine_fields = {
            'id': machine.id,
            'machine_id': machine.machine_id,
            'is_busy': machine.is_busy(),
            'auto_update': machine.auto_version,
            'current_agent_version':
                    {'id': current_av.id,
                     'name': current_av.name,
                     'updater_link': current_av.updater_link(),
                     'agent_link': current_av.agent_link(),

                     },
            'current_updater_version':
                    {'id': current_uv.id,
                     'name': current_uv.name,
                     'updater_link': current_uv.updater_link(),
                     'agent_link': current_uv.agent_link(),
                     },
            }

        return machine_fields

    if machine_id:
        return render_data("machine", build_event_fields(Machine.objects.get(machine_id=machine_id)))

    else:
        send_object = []
        for event in Machine.objects.all():
            send_object.append(build_event_fields(event))

        return render_data("machines", send_object)


@require_valid_api_token()
def get_schedules_for_machine(request, machine_id):
    def build_sql_backup(sql_backups):
        send_object = []
        for sql_backup in sql_backups:
            send_object.append(
                    {'id': sql_backup.id,
                     'host': sql_backup.host,
                     'username': sql_backup.username,
                     'password': sql_backup.password,
                     'database': sql_backup.database,
                     'type': sql_backup.type,
                     'port': sql_backup.port}
            )
        return send_object

    def build_folder_backup(folder_backups):
        send_object = []
        for folder_backup in folder_backups:
            send_object.append(
                    {'id': folder_backup.id,
                     'local_folder_path': folder_backup.local_folder_path,
                     }
            )
        return send_object

    def build_schedule_fields(schedule):
        schedule_fields = {
            'id': schedule.id,
            'name': schedule.name,
            'get_next_backup_time': schedule.get_next_backup_time(),
            'storage':
                    {'id': schedule.storage.id,
                     'host': schedule.storage.host,
                     'folder': schedule.storage.folder,
                     'current_day_folder_path': schedule.current_day_folder_path(),
                     },
            'running_backup': schedule.running_backup,
            'running_restore': schedule.running_restore,

            'sql_backups': build_sql_backup(schedule.sql_backups.all()),
            'folder_backups': build_folder_backup(schedule.folder_backups.all())


        }

        return schedule_fields

    send_object = []
    for schedule in Machine.objects.get(machine_id=machine_id).schedules.all():
        send_object.append(build_schedule_fields(schedule))

    return render_data("schedules", send_object)
