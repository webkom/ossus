# -*- coding: utf-8 -*-
from datetime import datetime
from app.backup.models import Company, Customer, Machine, Storage, ClientVersion, ScheduleBackup, FolderBackup, SQLBackup, Backup, MachineLog
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

example_date = datetime.strptime("2012-03-01 00:00:00", "%Y-%m-%d %H:%M:%S")

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
                agent_link="/",
                updater_link="/"
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

            for i in range(0, 3):
                storage = Storage.objects.get_or_create(type="Storage %s" % i, folder="backup/", company=company)[0]

            #Customers
            for i in range(0, 3):
                customer = Customer.objects.get_or_create(name="Customer %s" % i, company=company)[0]

                #Machines
                for k in range(0, 3):
                    machine = Machine.objects.get_or_create(
                        name="Machine %s " % i,
                        customer=customer,
                        last_connection_to_client=example_date,
                        machine_id=1000 + company.id + customer.id,
                        current_agent_version=versions[0],
                        current_updater_version=versions[0],
                        selected_agent_version=versions[0],
                        selected_updater_version=versions[0],
                    )[0]

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
                                datetime=example_date,
                                text="Running seed for this machine",
                                type="Type",
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
                                type="FTP %s" % o
                            )

            user.profile.set_company(user.companies.all()[0])