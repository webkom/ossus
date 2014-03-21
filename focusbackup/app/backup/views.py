# -*- coding: utf-8 -*-
import datetime

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.utils.translation import ugettext as _
from focusbackup.app.backup.forms import ScheduleForm, ScheduleFoldersForm, ScheduleSQLsForm

from focusbackup.app.backup.models import Schedule


@login_required()
def new(request, machine_id):
    return form(request, machine_id)


@login_required()
def edit(request, machine_id, id):
    return form(request, machine_id, id)


@login_required()
def form(request, machine_id, id=False):
    schedule = Schedule()

    machine = request.user.profile.get_machine_or_change_company(id=machine_id)
    title = "New schedule"

    def next_from_date():
        next = datetime.datetime.now() + datetime.timedelta(days=1)
        return next.strftime("%Y-%m-%d") + " 02:00:00"

    initial_data = {'from_date': next_from_date()}

    if id:
        schedule = request.user.profile.get_schedules().get(id=id)
        title = _("Schedule %s " % schedule.name)
        initial_data = {}

    form = ScheduleForm(instance=schedule, initial=initial_data, user=request.user)
    form_folders = ScheduleFoldersForm(instance=schedule, prefix="folders")
    form_sql = ScheduleSQLsForm(instance=schedule, prefix="sql")

    if request.method == "POST":
        form = ScheduleForm(request.POST, instance=schedule, initial=initial_data, user=request.user)
        form_folders = ScheduleFoldersForm(request.POST, prefix="folders", instance=schedule)
        form_sql = ScheduleSQLsForm(request.POST, prefix="sql", instance=schedule)

        if form.is_valid() and form_folders.is_valid() and form_sql.is_valid():
            schedule = form.save(commit=False)
            schedule.machine = machine

            schedule.save()
            form_folders.save()
            form_sql.save()

            if machine.template:
                return redirect("templates.view", machine.id)
            else:
                return redirect("machines.view", machine.id)

    return render(request, 'backup/form.html', {'form': form,
                                                'machine': machine,
                                                'form_folders': form_folders,
                                                'form_sql': form_sql,
                                                'title': title})