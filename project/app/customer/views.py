from app.customer.forms import CustomerForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.utils.translation import ugettext as _
from app.backup.models import Customer

@login_required()
def overview(request):
    customers = Customer.objects.filter(company=request.user.profile.company)
    return render(request, "customers/list.html", locals())


@login_required()
def view(request, id):
    customer = Customer.objects.get(id=id)
    return render(request, 'customers/view.html', locals())


def create(request):
    return form(request)


def edit(request, id):
    return form(request, id)


def form(request, id=False):
    instance = Customer()

    if id:
        instance = Customer.objects.get(id=id)

    form = CustomerForm(instance=instance)

    if request.method == "POST":
        form = CustomerForm(request.POST, instance=instance)

        if form.is_valid():
            customer = form.save(commit=False)
            customer.company = request.user.profile.company
            customer.save()

            return redirect(view, customer.id)

    return render(request, 'customers/form.html', {'form': form, "title": _("Server")})