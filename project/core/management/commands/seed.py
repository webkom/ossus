# -*- coding: utf-8 -*-
from datetime import datetime
from random import randint
import re
from app.backup.models import Company, Customer, Machine, Storage, ClientVersion, ScheduleBackup
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

        storage = None

        #Create client versions
        for j in range(0, randint(3,4)):
            ClientVersion.objects.get_or_create(name="Version %s"%j, agent_link="/", updater_link="/")

        #Create companies, with storage, customers and machines
        for j in range(0, randint(3,4)):
            company = Company.objects.get_or_create(name="Company %s"%j)[0]
            company.users.add(user)
            company.save()

            for i in range(0,randint(1,3)):
                storage = Storage.objects.get_or_create(type="Storage %s"%i, folder="backup/", company=company)[0]

            #Create customers
            for i in range(0,randint(1,3)):
                customer = Customer.objects.get_or_create(name="Customer %s"%i, company=company)[0]
                customer.save()

                #Machines
                for k in range(0,randint(1,3)):
                    machine = Machine.objects.get_or_create(name="Machine %s "%i, customer=customer)[0]
                    machine.machine_id = 1000+company.id+customer.id+machine.id
                    machine.last_connection_to_client = datetime.now()
                    machine.save()

                    #Schedules
                    for l in range(0,randint(1,3)):
                        scheduleBackup = ScheduleBackup.objects.get_or_create(  name="Schedule %s "%i,
                                                                                storage = storage,
                                                                                machine=machine,
                                                                                from_date = datetime.now(),
                                                                                last_run_time = datetime.now(),
                                                                                current_version_in_loop=1,
                                                                                versions_count = 10,
                                                                                repeat_every_minute = 30,
                        )[0]

                        scheduleBackup.save()

        user.profile.set_company(user.companies.all()[0])