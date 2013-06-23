# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.db import models


class Company(models.Model):
    name = models.CharField(max_length=150)
    users = models.ManyToManyField(User, related_name="companies")

    def __unicode__(self):
        return "Company: %s" % self.name