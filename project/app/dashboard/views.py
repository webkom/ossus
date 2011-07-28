from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from app.backup.models import Customer, Company

@login_required()
def overview(request):
    return render(request, "dashboard/dashboard.html")

@login_required()
def view_machine(request, machine_id):
    return render(request, "dashboard/machine/view.html", {'machine_id':machine_id})