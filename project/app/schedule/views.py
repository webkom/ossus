from django.contrib.auth.decorators import login_required
from django.forms.models import modelformset_factory
from django.shortcuts import render, redirect
from django.utils.translation import ugettext as _
from app.backup.models import ScheduleBackup
from app.schedule.forms import ScheduleBackupForm, ScheduleFoldersForm, ScheduleSQLsForm
from app.machine.views import view as machine_view

@login_required()
def new(request, machine_id):
    return form(request, machine_id)


@login_required()
def edit(request, machine_id, id):
    return form(request, machine_id, id)


@login_required()
def form(request, machine_id, id=False):
    title = _("Schedules")

    schedule = ScheduleBackup()
    machine = request.user.profile.get_machines().get(id=machine_id)

    if id:
        schedule = request.user.profile.get_schedules().get(id=id)

    form = ScheduleBackupForm(instance=schedule, user=request.user)
    form_folders = ScheduleFoldersForm(instance=schedule, prefix="folders")
    form_sql = ScheduleSQLsForm(instance=schedule, prefix="sql")

    if request.method == "POST":
        form = ScheduleBackupForm(request.POST, instance=schedule, user=request.user)
        form_folders = ScheduleFoldersForm(request.POST, prefix="folders", instance=schedule)
        form_sql = ScheduleSQLsForm(request.POST, prefix="sql", instance=schedule)

        if form.is_valid() and form_folders.is_valid() and form_sql.is_valid():
            schedule = form.save(commit=False)
            schedule.machine = machine

            schedule.save()
            form_folders.save()
            form_sql.save()

            return redirect(machine_view, machine.id)

    return render(request, 'schedule/form.html', locals())