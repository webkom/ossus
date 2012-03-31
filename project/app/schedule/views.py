from django.contrib.auth.decorators import login_required
from django.forms.models import modelformset_factory
from django.shortcuts import render, redirect
from django.utils.translation import ugettext as _
from app.backup.models import ScheduleBackup, Company, FolderBackup
from app.schedule.forms import ScheduleBackupForm
from app.machine.views import view as machine_view

@login_required()
def new(request, machine_id):
    return form(request, machine_id)

@login_required()
def edit(request, machine_id, id):
    return form(request, machine_id, id)

@login_required()
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


    folder_form = modelformset_factory(FolderBackup)(queryset=FolderBackup.objects.filter(schedule_backup=instance))



    return render(request, 'schedule/form.html', {'form': form, 'folder_form':folder_form, "title": _("Schedule")})