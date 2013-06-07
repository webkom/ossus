# -*- coding: utf-8 -*-
from datetime import datetime
from random import random, randint
from focusbackup.app.backup.models import Company, Customer, Machine, Storage, ClientVersion, ScheduleBackup, FolderBackup, SQLBackup, Backup, MachineLog, MachineStats
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.utils.timezone import utc

example_date = datetime.now()

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        admin_user = User.objects.get_or_create(username="admin")[0]
        admin_user.set_password("admin")
        admin_user.is_superuser = True
        admin_user.is_staff = True
        admin_user.save()

        storage = None
        versions = []

        #Create client versions
        for j in range(0, 4):
            version = ClientVersion.objects.get_or_create(
                name="Version %s" % j,
            )[0]

            version.set_current_agent()
            version.set_current_updater()
            versions.append(version)

        #Create companies, with storage, customers and machines
        for j in range(0, 4):
            company = Company.objects.get_or_create(name="Company %s" % j)[0]

            #Create test user for each company
            user = User.objects.get_or_create(username="test%s" % j)[0]
            user.set_password("test%s" % j)
            user.save()

            company.users.add(user)
            company.users.add(admin_user)

            user.profile.set_company(company)

            for i in range(0, 1):
                storage = Storage.objects.get_or_create(type="Storage %s" % i, host="81.167.228.94", username="backup", password="backup", folder="backup/", company=company)[0]

            #Customers
            for i in range(0, 3):
                customer = Customer.objects.get_or_create(name="Customer %s" % i, company=company)[0]

                #Machines
                for k in range(0, 3):
                    machine = Machine.objects.get_or_create(
                        name="Machine %s " % i,
                        customer=customer,
                        last_connection_to_client=example_date,
                        id=1000 + company.id + customer.id,
                        current_agent_version=versions[0],
                        current_updater_version=versions[0],
                        selected_agent_version=versions[0],
                        selected_updater_version=versions[0],
                    )[0]

                    #MachineStats data
                    for msi in range(0, 30):
                        cpu_system = randint(40, 50)

                        MachineStats.objects.get_or_create(
                            machine=machine,
                            load_average=random(),
                            cpu_system=cpu_system,
                            cpu_user=cpu_system - randint(15, 35),
                            cpu_stolen=cpu_system - randint(25, 35),
                            mem_used=randint(0, 20),
                            mem_free=randint(20, 40),
                        )

                    #Schedules
                    for l in range(0, 3):
                        scheduleBackup = ScheduleBackup.objects.get_or_create(
                            name="Schedule %s " % l,
                            storage=storage,
                            machine=machine,
                            from_date=example_date,
                            last_run_time=example_date,
                        )[0]

                        #Backups
                        for o in range(0, 3):
                            Backup.objects.get_or_create(
                                machine=machine,
                                schedule=scheduleBackup,
                                time_started=machine.last_connection_to_client,
                                day_folder_path=scheduleBackup.current_day_folder_path()
                            )

                        #Logs
                        for o in range(0, 3):
                            MachineLog.objects.get_or_create(
                                machine=machine,
                                datetime=datetime.now(),
                                text="Running seed for this machine",
                                type="INFO",
                            )

                        #FolderBackups
                        for o in range(0, 3):
                            FolderBackup.objects.get_or_create(
                                schedule_backup=scheduleBackup,
                                local_folder_path="/%s" % o
                            )

                        #SQLBackups
                        for o in range(0, 3):
                            SQLBackup.objects.get_or_create(
                                schedule_backup=scheduleBackup,
                                type="mysql",
                                host="192.168.0.%s" % o,
                                port="330%s" % o,
                                username="username %s" % o,
                                password="pw %s" % o,
                                database="database %s" % o,
                            )

            user.profile.set_company(user.companies.all()[0])