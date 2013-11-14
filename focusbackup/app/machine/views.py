# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.utils.translation import ugettext as _

from focusbackup.app.backup.models import Machine
from focusbackup.app.machine.forms import MachineForm


@login_required()
def overview(request):
    customers = request.user.profile.get_customers()

    return render(request, "machine/list.html", {
        'customers': customers,
        'title': 'List all servers'}
    )


@login_required()
def view(request, id):
    machine = request.user.profile.get_machines().get(id=id)
    return render(request, 'machine/view.html', {'machine': machine})


@login_required()
def view_log(request, id):
    machine = request.user.profile.get_machines().get(id=id)
    logs = machine.logs.all()[0:1000]
    return render(request, 'machine/log.html', {'machine': machine,
                                                'logs': logs})


@login_required()
def view_schedules(request, id):
    machine = request.user.profile.get_machines().get(id=id)
    schedules = machine.schedules.all()
    return render(request, 'machine/view_schedules.html', {'machine': machine,
                                                           'schedules': schedules})


@login_required()
def view_backups(request, id):
    machine = request.user.profile.get_machines().get(id=id)
    backups = machine.backups.all()
    return render(request, 'machine/view_backups.html', {'machine': machine,
                                                         'backups': backups})


@login_required()
def new(request):
    return form(request)


@login_required()
def edit(request, id):
    return form(request, id)


@login_required()
def form(request, id=False):
    instance = Machine()

    if id:
        instance = request.user.profile.get_machines().get(id=id)

    form = MachineForm(instance=instance, user=request.user)

    if request.method == "POST":
        form = MachineForm(request.POST, instance=instance, user=request.user)

        if form.is_valid():
            instance = form.save(commit=False)
            instance.save()

            return redirect(view, instance.id)

    return render(request, 'machine/form.html', {'form': form, "title": _("Server")})

