from datetime import datetime
import json
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from focusbackup.api.auth import require_valid_api_token
from focusbackup.api.forms.logs import LogAPIForm
from focusbackup.api.views.common import render_data, HandleQuerySets
from focusbackup.api.views.helpers import build_schedule_fields, build_machine_fields, build_machine_log, build_client_version, build_machine_log_fields, build_machine_settings
from focusbackup.app.backup.models import Machine, MachineLog, ClientVersion

@require_valid_api_token()
def get_machines(request, id=False):
    if id:
        return render_data("machine", build_machine_fields(Machine.objects.get(id=id)))

    else:
        send_object = []
        for event in Machine.objects.all():
            send_object.append(build_machine_fields(event))

        return render_data("machines", send_object)

get_machines = csrf_exempt(get_machines)

@require_valid_api_token()
def get_log_for_machine(request, id):
    return render_data("machine_log",
        build_machine_log(Machine.objects.get(id=id).logs.all().order_by("-id")))

get_log_for_machine = csrf_exempt(get_log_for_machine)

@require_valid_api_token()
def get_settings_for_machine(request, id):
    return render_data("",
        build_machine_settings(request, Machine.objects.get(id=id)))

get_log_for_machine = csrf_exempt(get_settings_for_machine)

@require_valid_api_token()
def set_machine_agent_version(request, id, version):
    client_version = ClientVersion.objects.get(id=version)

    if id:
        machine = Machine.objects.get(id=id)
        machine.current_agent_version = client_version
        machine.save()

    return render_data("client_version", build_client_version(client_version))

set_machine_agent_version = csrf_exempt(set_machine_agent_version)

@require_valid_api_token()
def set_machine_external_ip(request, id, ip_address):
    machine = Machine.objects.get(id=id)
    machine.external_ip = ip_address
    machine.save()

    return render_data("machine", build_machine_fields(machine))

set_machine_external_ip = csrf_exempt(set_machine_external_ip)

@require_valid_api_token()
def set_machine_updater_version(request, id, version):
    client_version = ClientVersion.objects.get(id=version)

    if id:
        machine = Machine.objects.get(id=id)
        machine.current_updater_version = client_version
        machine.save()

    return render_data("client_version", build_client_version(client_version))

set_machine_updater_version = csrf_exempt(set_machine_updater_version)

@require_valid_api_token()
def create_log_for_machine(request, id):
    if id:
        machine = Machine.objects.get(id=id)


        if request.method == "POST":
            form = LogAPIForm(request.POST)

            machine.set_last_connection_to_client()

            if form.is_valid():

                machine_log = MachineLog(machine=machine, datetime=datetime.now(), type=request.POST['type'],
                    text=request.POST['text'])

                machine_log.save()

                return render_data("log", {'log': build_machine_log_fields(machine_log)})

    return render_data("ERROR", {'error': 'No machine or not a valid form'})

create_log_for_machine = csrf_exempt(create_log_for_machine)

@require_valid_api_token()
def get_schedules_for_machine(request, id):
    send_object = []
    for schedule in Machine.objects.get(id=id).schedules.all():
        send_object.append(build_schedule_fields(schedule))

    return render_data("schedules", send_object)

get_schedules_for_machine = csrf_exempt(get_schedules_for_machine)