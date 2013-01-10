from datetime import datetime
from django.views.decorators.csrf import csrf_exempt
from api.auth import require_valid_api_token
from api.forms.machinestats import MachineStatsForm
from api.views.common import render_data
from app.backup.models import Machine, MachineStats

@require_valid_api_token()
def create_stats_for_machine(request, id):

    if id:
        machine = Machine.objects.get(id=id)

        if request.method == "POST":
            form = MachineStatsForm(request.POST, instance=MachineStats())
            if form.is_valid():
                log = form.save(commit=False)
                log.machine = machine
                log.datetime = datetime.now()
                log.save()

                machine.set_last_connection_to_client()

            return render_data("stats", {'id': log.id})

    return render_data("error", {'error':'invalid form'})


create_stats_for_machine = csrf_exempt(create_stats_for_machine)