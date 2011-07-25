from app.backup.models import Machine
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

@login_required()
def overview(request):
    machines = Machine.objects.all()
    return render(request, 'machines/list.htm', {'machines':machines})

@login_required()
def view(request, id):
    machine = Machine.objects.get(id=id)
    return render(request, 'machines/view.htm', {'machine':machine})