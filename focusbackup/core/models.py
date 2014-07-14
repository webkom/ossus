# -*- coding: utf-8 -*-
import random
from django.contrib.auth.models import User
from django.core.cache import cache
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

    class Meta:
        ordering = ["id"]

    def set_company(self, company):
        cache.set("user_profile_for_%s" % self.user.id, None)

        self.company = company
        self.save()

    def get_companies(self):
        cache_key = "user_%s_companies" % self.user.id
        companies = cache.get(cache_key)

        if companies:
            return companies

        company_ids = set([])

        for company in Company.objects.all().prefetch_related("users").select_related("users__profile"):
            if self.user.id in company.users.all().values_list("id", flat=True):
                company_ids.add(int(company.id))

        companies = list(Company.objects.filter(id__in=company_ids).prefetch_related("users").select_related("users__profile"))
        cache.set(cache_key, companies)

        return companies

    def get_customers(self):
        return Customer.objects.filter(company=self.company).prefetch_related("machines")

    def get_machine_or_change_company(self, id):
        try:
            return self.get_all_machines().get(id=id)
        except Machine.DoesNotExist:
            machine = Machine.objects.get(id=id)

            if machine.customer.company in self.get_companies():
                self.company = machine.customer.company
                self.save()

                return machine

            raise Machine.DoesNotExist

    def get_all_machines(self):
        machine_ids = []

        for customer in self.get_customers():
            for machine_id in customer.machines.all().values_list("id", flat=True).distinct():
                machine_ids.append(machine_id)

        return Machine.objects.filter(id__in=machine_ids).select_related("current_agent_version",
                                                                         "current_updater_version")

    def get_all_active_machines(self):
        return self.get_all_machines().filter(active=True)

    def get_machines(self):
        return self.get_all_machines().filter(template=False)

    def get_templates(self):
        return self.get_all_machines().filter(template=True)

    def get_storages(self):
        return Storage.objects.filter(company=self.company)

    def get_token(self):
        return Token.objects.get_or_create(api_user=self.user, active=True)[0]

    def get_schedules(self):
        schedule_ids = []

        for machine in self.get_all_machines():
            for schedule in machine.schedules.all():
                schedule_ids.append(schedule.id)

        return Schedule.objects.filter(id__in=schedule_ids)


def _get_user_profile(u):
    cache_key = "user_profile_for_%s" % u.id
    profile = cache.get(cache_key)

    if profile:
        return profile

    profile = UserProfile.objects.select_related("user", "company").get(user=u)
    cache.set(cache_key, profile)

    return profile

try:
    User.profile = property(lambda u: _get_user_profile(u))

except UserProfile.DoesNotExist:
    User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])