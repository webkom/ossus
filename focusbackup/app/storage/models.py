# -*- coding: utf-8 -*-
from django.db import models

from focusbackup.app.accounts.models import Company


storage_types = (
    ('ftp', 'FTP'),
)


class Storage(models.Model):
    type = models.CharField(max_length=10, choices=storage_types)
    company = models.ForeignKey(Company, related_name="storages", null=True)

    name = models.CharField(max_length=100, default="")
    notes = models.TextField(default="")

    host = models.CharField(max_length=150)
    username = models.CharField(max_length=80)
    password = models.CharField(max_length=80)

    #FTP folder or S3 bucket
    folder = models.CharField(max_length=255)

    class Meta:
        ordering = ["name"]

    def __unicode__(self):
        return "Storage: %s %s, Company %s" % (self.type, self.host, self.company)