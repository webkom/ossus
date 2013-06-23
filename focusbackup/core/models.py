# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.db import models

from focusbackup.api.models import Token
from focusbackup.app.accounts.models import Company
from focusbackup.app.backup.models import Schedule
from focusbackup.app.customer.models import Customer
from focusbackup.app.machine.models import Machine
from focusbackup.app.storage.models import Storage


class UserProfile(models.Model):
    user = models.ForeignKey(User, unique=True)
    company = models.ForeignKey(Company, blank=True, null=True)

    def set_company(self, company):
        self.company = company
        self.save()

    def get_companies(self):
        company_ids = []
        for company in Company.objects.all():
            if self.user in company.users.all():
                company_ids.append(company.id)

        return Company.objects.filter(id__in=company_ids)

    def get_customers(self):
        return Customer.objects.filter(company=self.company)

    def get_machines(self):
        machine_ids = []

        for customer in self.get_customers():
            for machine in customer.machines.all():
                machine_ids.append(machine.id)

        return Machine.objects.filter(id__in=machine_ids)

    def get_storages(self):
        return Storage.objects.filter(company=self.company)

    def get_token(self):
        return Token.objects.get_or_create(api_user=self.user, active=True)[0]

    def get_schedules(self):
        schedule_ids = []

        for machine in self.get_machines():
            for schedule in machine.schedules.all():
                schedule_ids.append(schedule.id)

        return Schedule.objects.filter(id__in=schedule_ids)

User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])