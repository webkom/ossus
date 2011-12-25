from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from app.backup.models import Machine, Company
from app.machine.forms import MachineForm

@login_required()
def overview(request):
    companies = Company.objects.all()
    return render(request, "machines/list.html", {'companies':companies})

@login_required()
def view(request, id):
    machine = Machine.objects.get(id=id)
    return render(request, 'machines/view.html', {'machine':machine})

def create(request):
    return form(request)

def edit(request, id):
    return form(request, id)

def form(request, id = False):

    instance = Machine()

    if id:
        instance = Machine.objects.get(id=id)

    form = MachineForm(instance=instance)

    if request.method == "POST":
        form = MachineForm(request.POST, instance=instance)

        if form.is_valid():
            form.save()

    return render(request, 'form.html', {'form':form})