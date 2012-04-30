from datetime import datetime
from random import random
import hashlib
from app.backup.models import Company, Customer, Machine, Storage, ScheduleBackup
from django.contrib.auth.models import User
from django.db import models

class UserProfile(models.Model):
    user = models.ForeignKey(User, unique=True)
    company = models.ForeignKey(Company, blank=True, null=True)
    api_token = models.CharField(max_length=255, default="0")

    def generate_api_token(self):
        self.api_token = hashlib.sha1(random.randint(14054,34023423))
        self.save()

    def get_api_token(self):
        if not self.api_token or self.api_token == "0":
            self.generate_api_token()
        return self.api_token

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

    def get_schedules(self):
        schedule_ids = []

        for machine in self.get_machines():
            for schedule in machine.schedules.all():
                schedule_ids.append(schedule.id)

        return ScheduleBackup.objects.filter(id__in=schedule_ids)

User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])
User.api_token = property(lambda u: UserProfile.objects.get_or_create(user=u)[0].get_api_token())