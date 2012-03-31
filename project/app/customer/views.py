from app.customer.forms import CustomerForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.utils.translation import ugettext as _
from app.backup.models import Customer

@login_required()
def overview(request):
    customers = request.user.profile.get_customers().filter(company=request.user.profile.company)
    return render(request, "customer/list.html", locals())


@login_required()
def view(request, id):
    customer = request.user.profile.get_customers().get(id=id)
    return render(request, 'customer/view.html', locals())


@login_required()
def new(request):
    return form(request)


@login_required()
def edit(request, id):
    return form(request, id)


@login_required()
def form(request, id=False):
    instance = Customer()

    if id:
        instance = request.user.profile.get_customers().get(id=id)

    form = CustomerForm(instance=instance)

    if request.method == "POST":
        form = CustomerForm(request.POST, instance=instance)

        if form.is_valid():
            customer = form.save(commit=False)
            customer.company = request.user.profile.company
            customer.save()

            return redirect(view, customer.id)

    return render(request, 'customer/form.html', {'form': form, "title": _("Server")})