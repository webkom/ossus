# -*- coding: utf-8 -*-
from django.db import models


class ClientVersion(models.Model):
    datetime = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=50)

    agent = models.FileField(upload_to="versions/agents/", null=True)
    updater = models.FileField(upload_to="versions/updaters/", null=True)

    current_agent = models.BooleanField(default=False)
    current_updater = models.BooleanField(default=False)

    def __unicode__(self):
        return self.name

    def agent_link(self):
        if self.agent:
            return self.agent.url
        return ""

    def updater_link(self):
        if self.updater:
            return self.updater.url
        return ""

    def set_current_agent(self):
        for v in ClientVersion.objects.all():
            v.current_agent = False
            v.save()

        self.current_agent = True
        self.save()

    def set_current_updater(self):
        for v in ClientVersion.objects.all():
            v.current_updater = False
            v.save()

        self.current_updater = True
        self.save()
