from django.shortcuts import render

def overview(request):
    return render(request, "dashboard/overview.html")

def view_machine(request, machine_id):
    return render(request, "dashboard/view_machine.html", {'machine_id':machine_id})