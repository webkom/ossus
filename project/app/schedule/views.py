from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.utils.translation import ugettext as _
from app.backup.models import ScheduleBackup, Company
from app.schedule.forms import ScheduleBackupForm
from app.machine.views import view as machine_view

def new(request, machine_id):
    return form(request, machine_id)

def edit(request, machine_id, id):
    return form(request, machine_id, id)

def form(request, machine_id, id=False):
    instance = ScheduleBackup()

    machine = request.user.profile.get_machines().get(id=machine_id)

    if id:
        instance = request.user.profile.get_schedules().get(id=id)

    form = ScheduleBackupForm(instance=instance, user=request.user)

    if request.method == "POST":
        form = ScheduleBackupForm(request.POST, instance=instance, user=request.user)

        if form.is_valid():
            instance = form.save(commit=False)
            instance.machine = machine

            instance.save()

            return redirect(machine_view, machine.id)

    return render(request, 'schedule/form.html', {'form': form, "title": _("Schedule")})