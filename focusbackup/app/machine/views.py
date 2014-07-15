# -*- coding: utf-8 -*-
import datetime
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.utils.translation import ugettext as _
from focusbackup.api.views.common import render_data
from focusbackup.api.views.helpers import build_machine_settings

from focusbackup.app.backup.models import Machine
from focusbackup.app.client.models import ClientVersion
from focusbackup.app.machine.forms import MachineForm


@login_required()
def overview(request):
    customers = request.user.profile.get_customers()

    return render(request, "machine/list.html", {
        'customers': customers,
        'title': 'List all servers'}
    )


@login_required()
def templates(request):
    return render(request, "machine/templates/list.html", {
        'templates': request.user.profile.get_templates(),
        'title': 'List all templates'}
    )


@login_required()
def view(request, id):
    machine = request.user.profile.get_machine_or_change_company(id=id)
    return render(request, 'machine/view.html', {'machine': machine,
                                                 'title': machine.name})


@login_required()
def view_template(request, id):
    machine = request.user.profile.get_machine_or_change_company(id=id)
    return render(request, 'machine/templates/view.html', {'machine': machine,
                                                           'title': machine.name})


@login_required()
def replace_schedules_with_template(request, id, template_id):
    template = request.user.profile.get_templates().get(id=template_id)
    template_clone = template.clone()

    machine = request.user.profile.get_all_machines().get(id=id)

    machine.schedules.all().delete()

    for schedule in template_clone.schedules.all():
        schedule.machine = machine
        schedule.save()

    template_clone.delete()

    return render(request, 'machine/templates/view.html', {'machine': machine,
                                                           'title': machine.name})


@login_required()
def view_template_schedules(request, id):
    machine = request.user.profile.get_machine_or_change_company(id=id)
    schedules = machine.schedules.all()
    return render(request, 'machine/templates/schedules.html', {'machine': machine,
                                                                'schedules': schedules,
                                                                'title': machine.name})


@login_required()
def view_log(request, id):
    machine = request.user.profile.get_machine_or_change_company(id=id)
    logs = machine.logs.all().order_by("-id")[0:300]
    return render(request, 'machine/log.html', {'machine': machine,
                                                'logs': logs,
                                                'title': machine.name})


@login_required()
def view_schedules(request, id):
    machine = request.user.profile.get_machine_or_change_company(id=id)
    schedules = machine.schedules.all()
    return render(request, 'machine/view_schedules.html', {'machine': machine,
                                                           'schedules': schedules,
                                                           'title': machine.name})


@login_required()
def install_instructions(request):
    return render(request, 'machine/install_instructions.html')


@login_required()
def install_instructions_linux(request):
    return render(request, 'machine/install_instructions_linux.html')


@login_required()
def view_backups(request, id):
    machine = request.user.profile.get_machine_or_change_company(id=id)
    backups = machine.backups.all().prefetch_related("schedules")

    return render(request, 'machine/view_backups.html', {'machine': machine,
                                                         'backups': backups,
                                                         'title': machine.name})


@login_required()
def all_recoverable_backups_schedule(request, id, schedule_id):
    machine = request.user.profile.get_machine_or_change_company(id=id)
    schedule = machine.schedules.get(id=schedule_id)
    backups = schedule.get_recoverable_backups(schedule.versions_count)

    return render(request, 'machine/list_backups.html', {'machine': machine,
                                                         'schedule': schedule,
                                                         'backups': backups,
                                                         'title': machine.name})

@login_required()
def settings(request, id):
    return render_data("", build_machine_settings(request, Machine.objects.get(id=id)))


@login_required()
def toggle_busy(request, id):
    machine = request.user.profile.get_machine_or_change_company(id=id)

    if machine.lock:
        machine.lock = None
        machine.lock_session = None
        machine.log("info", "%s release lock trough interface" % request.user.get_full_name())
    else:
        machine.lock = datetime.datetime.now()
        machine.lock_session = None
        machine.log("info", "%s put lock trough web interface" % request.user.get_full_name())

    machine.save()

    return redirect(view, id)


@login_required()
def toggle_run_schedule_now(request, id, schedule_id):
    machine = request.user.profile.get_machine_or_change_company(id=id)
    schedule = machine.schedules.get(id=schedule_id)
    schedule.run_now = not schedule.run_now
    schedule.save()

    return redirect(view_schedules, id)


@login_required()
def stop_schedule(request, id, schedule_id):
    machine = request.user.profile.get_machine_or_change_company(id=id)
    schedule = machine.schedules.get(id=schedule_id)
    schedule.running_backup = False
    schedule.save()

    return redirect(view_schedules, id)


@login_required()
def toggle_active(request, id):
    machine = request.user.profile.get_machine_or_change_company(id=id)
    machine.active = not machine.active
    machine.save()

    return redirect(view, id)


@login_required()
def new(request):
    return form(request)


@login_required()
def edit(request, id):
    return form(request, id)


@login_required()
def delete(request, id):
    instance = request.user.profile.get_machine_or_change_company(id=id)
    instance.delete()
    return redirect(overview)


@login_required()
def form(request, id=False):
    instance = Machine()

    if id:
        instance = request.user.profile.get_machine_or_change_company(id=id)

    form = MachineForm(instance=instance, user=request.user)

    if request.method == "POST":
        form = MachineForm(request.POST, instance=instance, user=request.user)

        if form.is_valid():
            instance = form.save(commit=False)

            if not instance.id:
                instance.current_agent_version = ClientVersion.objects.get(current_agent=True)
                instance.current_updater_version = ClientVersion.objects.get(current_updater=True)

            instance.save()

            return redirect(view, instance.id)

    return render(request, 'machine/form.html', {'form': form, "title": _("Server")})

