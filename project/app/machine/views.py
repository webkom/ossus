from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.utils.translation import ugettext as _
from app.backup.models import Machine, Company
from app.machine.forms import MachineForm

@login_required()
def overview(request):
    customers = request.user.profile.get_customers()
    return render(request, "machine/list.html", locals())

@login_required()
def view(request, id):
    machine = request.user.profile.get_machines().get(id=id)
    return render(request, 'machine/view.html', {'machine':machine})

@login_required()
def new(request):
    return form(request)

@login_required()
def edit(request, id):
    return form(request, id)

@login_required()
def form(request, id = False):

    instance = Machine()

    if id:
        instance = request.user.profile.get_machines().get(id=id)

    form = MachineForm(instance=instance, user=request.user)

    if request.method == "POST":
        form = MachineForm(request.POST, instance=instance, user=request.user)

        if form.is_valid():
            instance = form.save(commit=False)
            instance.save()

            return redirect(view, instance.id)

    return render(request, 'machine/form.html', {'form':form, "title":_("Server")})

