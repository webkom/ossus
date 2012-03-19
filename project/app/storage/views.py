from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils.translation import ugettext as _
from app.backup.models import Storage, Company
from app.storage.forms import StorageForm

@login_required()
def overview(request):
    companies = Company.objects.all()
    return render(request, "storages/list.html", {'companies':companies})

@login_required()
def view(request, id):
    storage = Storage.objects.get(id=id)
    return render(request, 'storages/view.html', {'storage':storage})

def new(request):
    return form(request)

def edit(request, id):
    return form(request, id)

def form(request, id = False):

    instance = Storage()

    if id:
        instance = Storage.objects.get(id=id)

    form = StorageForm(instance=instance)

    if request.method == "POST":
        form = StorageForm(request.POST, instance=instance)

        if form.is_valid():
            form.save()

    return render(request, 'storages/form.html', {'form':form, "title":_("Server")})