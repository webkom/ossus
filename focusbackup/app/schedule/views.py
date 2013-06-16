from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.utils.translation import ugettext as _
from focusbackup.app.backup.models import ScheduleBackup
from datetime import datetime, timedelta

@login_required()
def new(request, machine_id):
    return form(request, machine_id)

@login_required()
def edit(request, machine_id, id):
    return form(request, machine_id, id)

@login_required()
def form(request, machine_id, id=False):

    from focusbackup.app.schedule.forms import ScheduleBackupForm, ScheduleFoldersForm, ScheduleSQLsForm

    schedule = ScheduleBackup()

    machine = request.user.profile.get_machines().get(id=machine_id)
    title = "New schedule"

    def next_from_date():
        next = datetime.now()+timedelta(days=1)
        return next.strftime("%Y-%m-%d") + " 02:00:00"

    initial_data = {'from_date': next_from_date()}

    if id:
        schedule = request.user.profile.get_schedules().get(id=id)
        title = _("Schedule %s " % schedule.name)
        initial_data = {}

    form = ScheduleBackupForm(instance=schedule, initial=initial_data, user=request.user)
    form_folders = ScheduleFoldersForm(instance=schedule, prefix="folders")
    form_sql = ScheduleSQLsForm(instance=schedule, prefix="sql")

    if request.method == "POST":
        form = ScheduleBackupForm(request.POST, instance=schedule, initial=initial_data, user=request.user)
        form_folders = ScheduleFoldersForm(request.POST, prefix="folders", instance=schedule)
        form_sql = ScheduleSQLsForm(request.POST, prefix="sql", instance=schedule)

        if form.is_valid() and form_folders.is_valid() and form_sql.is_valid():
            schedule = form.save(commit=False)
            schedule.machine = machine

            schedule.save()
            form_folders.save()
            form_sql.save()

            return redirect("view_machine", machine.id)

    return render(request, 'schedule/form.html', locals())