# -*- coding: utf-8 -*-

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.utils.translation import ugettext as _

from focusbackup.app.backup.models import Storage
from focusbackup.app.storage.forms import StorageForm


@login_required()
def overview(request):
    storages = request.user.profile.get_storages().filter(company=request.user.profile.company)
    return render(request, "storage/list.html", locals())


@login_required()
def new(request):
    return form(request)


@login_required()
def edit(request, id):
    return form(request, id)


@login_required()
def form(request, id=False):
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

            return redirect(overview)

    return render(request, 'storage/form.html', {'form': form, "title": _("Storage")})