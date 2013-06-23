# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.shortcuts import HttpResponseRedirect
from focusbackup.app.accounts.models import Company


@login_required()
def change_company(request, id):
    company = Company.objects.get(id=id)

    if company in request.user.profile.get_companies():
        request.user.profile.set_company(company)

    return HttpResponseRedirect("/")