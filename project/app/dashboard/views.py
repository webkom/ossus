from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required()
def overview(request):
    return render(request, "dashboard/overview.html")

@login_required()
def view_machine(request, machine_id):
    return render(request, "dashboard/view_machine.html", {'machine_id':machine_id})