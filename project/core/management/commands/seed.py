# -*- coding: utf-8 -*-
from datetime import datetime
from random import randint
import re
from app.backup.models import Company, Customer, Machine, Storage, ClientVersion, ScheduleBackup, FolderBackup, SQLBackup
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from urllib import urlopen

class Command(BaseCommand):

    def handle(self, *args, **kwargs):

        admin_user = User.objects.get_or_create(username="admin")[0]
        admin_user.set_password("admin")
        admin_user.is_superuser = True
        admin_user.is_staff = True
        admin_user.save()

        storage = None
        version = None

        #Create client versions
        for j in range(0, randint(3,4)):
            version = ClientVersion.objects.get_or_create(name="Version %s"%j, agent_link="/", updater_link="/")[0]
            version.current_agent = True
            version.current_updater = True
            version.save()

        #Create companies, with storage, customers and machines
        for j in range(0,4):
            company = Company.objects.get_or_create(name="Company %s"%j)[0]

            #Create test user for each company
            user = User.objects.get_or_create(username="test%s"%j)[0]
            user.set_password("test%s"%j)
            user.save()

            company.users.add(user)
            company.users.add(admin_user)
            company.save()

            user.profile.set_company(company)


            for i in range(0,randint(1,3)):
                storage = Storage.objects.get_or_create(type="Storage %s"%i, folder="backup/", company=company)[0]

            #Customers
            for i in range(0,randint(1,3)):
                customer = Customer.objects.get_or_create(name="Customer %s"%i, company=company)[0]
                customer.save()

                #Machines
                for k in range(0,randint(1,3)):
                    machine = Machine.objects.get_or_create(name="Machine %s "%i, customer=customer)[0]
                    machine.machine_id = 1000+company.id+customer.id+machine.id
                    machine.last_connection_to_client = datetime.now()
                    machine.current_agent_version = version
                    machine.current_updater_version = version
                    machine.selected_agent_version = version
                    machine.selected_updater_version = version

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


                        #FolderBackups
                        for o in range(0,randint(1,3)):
                            folderBackup = FolderBackup.objects.get_or_create(schedule_backup = scheduleBackup,
                                                                              local_folder_path = "/")

                        #SQLBackups
                        for o in range(0,randint(1,3)):
                            folderBackup = SQLBackup.objects.get_or_create(schedule_backup = scheduleBackup,
                                                                            type = "FTP")



            user.profile.set_company(user.companies.all()[0])