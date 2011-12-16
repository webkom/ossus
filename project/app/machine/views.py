from app.backup.models import Machine, Company
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

@login_required()
def overview(request):
    companies = Company.objects.all()
    return render(request, "machines/list.html", {'companies':companies})

@login_required()
def view(request, id):
    machine = Machine.objects.get(id=id)
    return render(request, 'machines/view.html', {'machine':machine})