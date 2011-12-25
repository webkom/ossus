# -*- coding: utf-8 -*-
from app.accounts.forms import LoginForm
from django.shortcuts import render_to_response, redirect, HttpResponseRedirect
from django.conf import settings
from django.contrib.auth import authenticate, login, logout

def login_view(request):
    message = ""

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

    return render_to_response('login.html', {'form': form})

def logout_view(request):
    logout(request)
    return HttpResponseRedirect("/accounts/login/")