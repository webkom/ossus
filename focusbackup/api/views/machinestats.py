# -*- coding: utf-8 -*-
import datetime

from django.views.decorators.csrf import csrf_exempt

from focusbackup.api.auth import require_valid_api_token
from focusbackup.api.forms import MachineStatsForm
from focusbackup.api.views.common import render_data
from focusbackup.app.backup.models import Machine
from focusbackup.app.machine.models import MachineStats


@require_valid_api_token()
def create_stats_for_machine(request, id):
    if id and request.method == "POST":
        machine = Machine.objects.get(id=id)

        form = MachineStatsForm(request.POST, instance=MachineStats())

        if form.is_valid():
            stats = form.save(commit=False)
            stats.machine = machine
            stats.datetime = datetime.datetime.now()
            stats.save()

            return render_data("stats", {'id': stats.id})

    return render_data("error", {'error': 'invalid form'})

create_stats_for_machine = csrf_exempt(create_stats_for_machine)