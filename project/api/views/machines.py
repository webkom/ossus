from datetime import datetime
import json
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from api.auth import require_valid_api_token
from api.forms.logs import LogAPIForm
from api.views.common import render_data, HandleQuerySets
from api.views.helpers import build_schedule_fields, build_machine_fields, build_machine_log, build_client_version
from app.backup.models import Machine, MachineLog, ClientVersion

@require_valid_api_token()
def get_machines(request, machine_id=False):
    if machine_id:
        return render_data("machine", build_machine_fields(Machine.objects.get(machine_id=machine_id)))

    else:
        send_object = []
        for event in Machine.objects.all():
            send_object.append(build_machine_fields(event))

        return render_data("machines", send_object)

get_machines = csrf_exempt(get_machines)

@require_valid_api_token()
def get_log_for_machine(request, machine_id):
    return render_data("machine_log",
        build_machine_log(Machine.objects.get(machine_id=machine_id).logs.all().order_by("-id")))

get_log_for_machine = csrf_exempt(get_log_for_machine)

@require_valid_api_token()
def set_machine_agent_version(request, machine_id, version):
    client_version = ClientVersion.objects.get(id=version)

    if machine_id:

        machine = Machine.objects.get(machine_id=machine_id)
        machine.current_agent_version = client_version
        machine.save()

    return render_data("client_version", build_client_version(client_version))

set_machine_agent_version = csrf_exempt(set_machine_agent_version)

@require_valid_api_token()
def set_machine_updater_version(request, machine_id, version):
    client_version = ClientVersion.objects.get(id=version)

    if machine_id:

        machine = Machine.objects.get(machine_id=machine_id)
        machine.current_updater_version = client_version
        machine.save()

    return render_data("client_version", build_client_version(client_version))

set_machine_updater_version = csrf_exempt(set_machine_updater_version)

@require_valid_api_token()
def create_log_for_machine(request, machine_id):
    if machine_id:
        machine = Machine.objects.get(machine_id=machine_id)

        if request.method == "POST":
            form = LogAPIForm(request.POST)

            if form.is_valid():

                machine_log = MachineLog(machine=machine, datetime=datetime.now(), type=request.POST['type'],
                    text=request.POST['text'])

                machine_log.save()

    return render_data("hei", {'a': 'b'})

create_log_for_machine = csrf_exempt(create_log_for_machine)

@require_valid_api_token()
def get_schedules_for_machine(request, machine_id):
    send_object = []
    for schedule in Machine.objects.get(machine_id=machine_id).schedules.all():
        send_object.append(build_schedule_fields(schedule))

    return render_data("schedules", send_object)

get_schedules_for_machine = csrf_exempt(get_schedules_for_machine)