# -*- coding: utf-8 -*-
from django.views.decorators.csrf import csrf_exempt

from focusbackup.api.auth import RequireValidToken
from focusbackup.api.forms import ScheduleAPIForm
from focusbackup.api.views.common import render_data
from focusbackup.api.views.helpers import build_schedule_fields
from focusbackup.app.backup.models import Schedule


@RequireValidToken()
def get_schedules(request, id=False):
    send_object = []

    if id and request.method == "POST":

        schedule = Schedule.objects.get(id=id)
        form = ScheduleAPIForm(request.POST)

        if form.is_valid():

            schedule.name = form.cleaned_data['name']

            if form.cleaned_data['running_backup'] == "true":
                schedule.running_backup = True
            else:
                schedule.running_backup = False

            if form.cleaned_data['running_restore'] == "true":
                schedule.running_restore = True
            else:
                schedule.running_restore = False

            schedule.current_version_in_loop = int(form.cleaned_data['current_version_in_loop'])

            # Only set last_run when running_backup is true
            if schedule.running_backup:
                schedule.set_last_run_time()

            schedule.save(update_fields=["name", "running_backup",
                                         "running_restore", "current_version_in_loop"])

        return render_data("schedule", build_schedule_fields(schedule))

    for obj in Schedule.objects.all():
        send_object.append(build_schedule_fields(obj))

    return render_data("schedules", send_object)


get_schedules = csrf_exempt(get_schedules)
