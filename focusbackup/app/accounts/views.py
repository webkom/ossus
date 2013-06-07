# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, HttpResponseRedirect, render
from django.contrib.auth import authenticate, login, logout

from focusbackup.app.accounts.forms import LoginForm
from focusbackup.app.backup.models import Company


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)

        if form.is_valid():
            data = form.cleaned_data

            username = data['username']
            password = data['password']

            redirect_to = request.REQUEST.get('next', '')

            user = authenticate(username=username, password=password)

            if user is not None:
                if user.is_active:
                    login(request, user)

                    if not redirect_to:
                        return HttpResponseRedirect("/")

                    return HttpResponseRedirect('%s' % redirect_to)

                return render_to_response('login.html')
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})


@login_required()
def change_company(request, id):
    company = Company.objects.get(id=id)

    if company in request.user.profile.get_companies():
        request.user.profile.set_company(company)

    return HttpResponseRedirect("/")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect("/accounts/login/")