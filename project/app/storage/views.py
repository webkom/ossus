from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.utils.translation import ugettext as _
from app.backup.models import Storage, Company
from app.storage.forms import StorageForm

@login_required()
def overview(request):
    storages = request.user.profile.get_storages().filter(company = request.user.profile.company)
    return render(request, "storage/list.html", locals())

def new(request):
    return form(request)

def edit(request, id):
    return form(request, id)

def form(request, id = False):

    instance = Storage()

    if id:
        instance = request.user.profile.get_storages().get(id=id)

    form = StorageForm(instance=instance)

    if request.method == "POST":
        form = StorageForm(request.POST, instance=instance)

        if form.is_valid():
            storage = form.save(commit=False)
            storage.company = request.user.profile.company
            storage.save()

            return redirect(edit, storage.id)

    return render(request, 'storage/form.html', {'form':form, "title":_("Storage")})