# -*- coding: utf-8 -*-
from django.db import models

from focusbackup.app.accounts.models import Company


class Customer(models.Model):
    name = models.CharField(max_length=150)
    address = models.CharField(max_length=100, blank=True, null=True)
    contact_person = models.CharField(max_length=100, blank=True, null=True)
    contact_email = models.CharField(max_length=100, blank=True, null=True)
    contact_phone = models.CharField(max_length=20, blank=True, null=True)

    company = models.ForeignKey(Company, related_name="customers")

    class Meta:
        ordering = ["name"]

    def __unicode__(self):
        return self.name

    def get_machines(self):
        return self.machines.filter(template=False).select_related("current_agent_version",
                                                                   "current_updater_version")