# -*- coding: utf-8 -*-
from random import randint
import re
from app.backup.models import Company, Customer, Machine
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from urllib import urlopen

class Command(BaseCommand):

    def handle(self, *args, **kwargs):

        user = User.objects.get_or_create(username="test1")[0]
        user.set_password("test1")
        user.is_superuser = True
        user.is_staff = True
        user.save()

        for j in range(0, randint(3,4)):
            company = Company.objects.get_or_create(name="Company%s"%j)[0]
            company.users.add(user)
            company.save()

            for i in range(0,randint(1,3)):
                customer = Customer.objects.get_or_create(name="Customer%s"%i, company=company)[0]
                customer.save()

                for i in range(0,randint(1,3)):
                    machine = Machine.objects.get_or_create(name="Machine %s "%i, customer=customer)[0]
                    machine.machine_id = 1000+company.id+customer.id+machine.id
                    machine.save()

        user.profile.set_company(user.companies.all()[0])