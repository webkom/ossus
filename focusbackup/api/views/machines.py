# -*- coding: utf-8 -*-
import datetime
from django.db import transaction
from django.http import Http404
from django.shortcuts import get_object_or_404

from django.views.decorators.csrf import csrf_exempt

from focusbackup.api.auth import require_valid_api_token
from focusbackup.api.forms import LogAPIForm
from focusbackup.api.views.common import render_data
from focusbackup.api.views.helpers import build_schedule_fields, build_machine_fields, \
    build_machine_log, build_client_version, build_machine_log_fields, build_machine_settings
from focusbackup.app.client.models import ClientVersion
from focusbackup.app.machine.models import Machine, MachineLog


@require_valid_api_token()
def get_machines(request, id=False):
    try:
        if id:
            return render_data("machine", build_machine_fields(Machine.objects.get(id=id)))

        else:
            send_object = []
            for event in Machine.objects.all():
                send_object.append(build_machine_fields(event))

            return render_data("machines", send_object)
    except Machine.DoesNotExist:
        raise Http404


get_machines = csrf_exempt(get_machines)


@require_valid_api_token()
def get_log_for_machine(request, id):
    return render_data("machine_log",
                       build_machine_log(Machine.objects.get(id=id).logs.all().order_by("-id")))


get_log_for_machine = csrf_exempt(get_log_for_machine)


@require_valid_api_token()
def get_settings_for_machine(request, id):
    return render_data("", build_machine_settings(request, Machine.objects.get(id=id)))


get_settings_for_machine = csrf_exempt(get_settings_for_machine)


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
@transaction.atomic
def set_busy_updating(request, id, busy, client_session=None):

    machine = Machine.objects.get(id=id)
    machine.log("info", "session %s connecting...")
    machine.set_last_connection_to_client()

    if client_session and machine.lock_session and client_session != machine.lock_session:
        machine.log(
            "warning",
            "%s Attempt to %s machine, "
            "but the lock is set by another session, "
            "have to wait until the lock is released by %s" % (client_session,
                                                               "lock" if busy == '1' else 'unlock',
                                                               machine.lock_session)
        )

        change_status = False

    #is the current session the current locker
    elif client_session and machine.lock_session and client_session == machine.lock_session:

        if busy == '0':
            change_status = True
            machine.release_lock(client_session)
        else:
            change_status = False
            machine.log("warning",
                        "%s did not change the current lock, why did you try this?" % client_session)

    elif client_session and not machine.lock:

        if busy == '1':
            change_status = True
            machine.set_lock(client_session)
        else:
            change_status = False
            machine.log("warning",
                        "%s tried to unlock, but the machine is already unlocked.." % client_session)

    elif client_session and machine.lock:

        if busy == '0':
            change_status = True
            machine.release_lock(client_session)
        else:
            change_status = False
            machine.log("warning",
                        "%s tried to lock, but the machine is already locked.." % client_session)

    elif not client_session:
        machine.log("error", "the client did not provide a client session, will try my best..")

        if machine.lock and busy == '0':
            change_status = True
            machine.release_lock()

        elif not machine.lock and busy == '1':
            change_status = True
            machine.set_lock()

        else:
            change_status = False
            machine.log("warning", "unspecified session tried to set "
                                   "lock, but it did not "
                                   "change, current lock status is: %s "
                                   % "locked" if busy == '1' else 'unlocked')

    else:
        #do nothing..
        change_status = False
        machine.log("warning",
                    "no idea what to do.. this is what I know: lock: %s, "
                    "lock_session: %s, client_session: %s" % (machine.lock,
                                                              machine.lock_session,
                                                              client_session))

    return render_data("changed_status", change_status)

set_busy_updating = csrf_exempt(set_busy_updating)


@require_valid_api_token()
def deactivate(request, id):
    machine = Machine.objects.get(id=id)
    machine.active = False
    machine.save()

    return render_data("machine", build_machine_fields(machine))


deactivate = csrf_exempt(deactivate)


@require_valid_api_token()
def create_new_machine_from_template(request, id, name):
    template = get_object_or_404(Machine, id=id, template=True)
    machine = template.clone()

    machine.name = name
    machine.template = False
    machine.save()

    return render_data("machine", build_machine_fields(machine))


create_new_machine_from_template = csrf_exempt(create_new_machine_from_template)


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
                machine_log = MachineLog(machine=machine, datetime=datetime.datetime.now(),
                                         type=request.POST['type'],
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