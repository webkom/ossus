# -*- coding: utf-8 -*-
import datetime

from django.db import models

from focusbackup.app.client.models import ClientVersion
from focusbackup.app.customer.models import Customer


class Machine(models.Model):
    name = models.CharField(max_length=150)
    customer = models.ForeignKey(Customer, related_name="machines")
    run_install = models.BooleanField(default=False)

    #Info from the client
    last_connection_to_client = models.DateTimeField(blank=True, null=True, default=datetime.datetime.now())
    external_ip = models.IPAddressField(default="")

    #For generating settings-file
    local_temp_folder = models.CharField(max_length=255, default="C:\\focus24\\temp\\")
    agent_folder = models.CharField(max_length=255, default="C:\\focus24\\")
    mysql_dump = models.CharField(max_length=255, default="mysqldump")

    auto_version = models.BooleanField(default=True)

    updating_client = models.BooleanField(default=False)

    #Current version running on client
    current_agent_version = models.ForeignKey(ClientVersion, related_name="agent_versions", null=True)
    current_updater_version = models.ForeignKey(ClientVersion, related_name="updater_versions", null=True)

    #If not auto_version
    selected_agent_version = models.ForeignKey(ClientVersion, related_name="agent_selected", null=True, blank=True)
    selected_updater_version = models.ForeignKey(ClientVersion, related_name="updater_selected", null=True, blank=True)

    def __unicode__(self):
        return "Machine: %s, id: %s" % (self.name, self.id)

    def is_up_to_date(self):
        return self.current_agent_version == ClientVersion.objects.get(current_agent=True) and \
               self.current_updater_version == ClientVersion.objects.get(current_updater=True)

    def lost_connection_to_client(self):
        return datetime.datetime.now() - self.last_connection_to_client > datetime.timedelta(minutes=10)

    def set_last_connection_to_client(self):
        self.last_connection_to_client = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.save()

    def get_selected_agent_version(self):
        if self.auto_version:
            return ClientVersion.objects.get(current_agent=True)
        else:
            return self.selected_agent_version

    def get_selected_updater_version(self):
        if self.auto_version:
            return ClientVersion.objects.get(current_updater=True)
        else:
            return self.selected_updater_version

    def get_latest_stats(self):
        if self.stats.all().count() > 20:
            return self.stats.all().order_by("id")[self.stats.all().count() - 20:]

        return self.stats.all().order_by("id")

    def get_latest_logs(self):
        return self.logs.all().order_by("-id")[0:8]

    def get_latest_backups(self):
        return self.backups.all().order_by("-id")[0:8]

    def running_backup(self):
        for schedule in self.schedules.all():
            if schedule.running_backup:
                return True
        return False

    def running_restore(self):
        for schedule in self.schedules.all():
            if schedule.running_restore:
                return True
        return False

    def is_busy(self):
        return self.running_restore() or self.running_backup() or self.updating_client

    def get_last_backup_time(self):
        next_backup_time = None
        for schedule in self.schedules.all():
            if not next_backup_time:
                next_backup_time = schedule.get_last_backup_time()
            elif schedule.get_next_run_time() > next_backup_time:
                next_backup_time = schedule.get_last_backup_time()

        return next_backup_time

    def get_next_backup_time(self):
        next_backup_time = None
        for schedule in self.schedules.all():
            if not next_backup_time:
                next_backup_time = schedule.get_next_backup_time()
            elif schedule.get_next_backup_time() < next_backup_time:
                next_backup_time = schedule.get_next_backup_time()

        return next_backup_time


class MachineStats(models.Model):
    datetime = models.DateTimeField(default=datetime.datetime.now())
    machine = models.ForeignKey(Machine, related_name="stats")

    load_average = models.DecimalField(decimal_places=3, max_digits=50)

    cpu_system = models.DecimalField(decimal_places=3, max_digits=50)
    cpu_user = models.DecimalField(decimal_places=3, max_digits=50)
    cpu_stolen = models.DecimalField(decimal_places=3, max_digits=50)

    mem_used = models.DecimalField(decimal_places=3, max_digits=50, default=0)
    mem_free = models.DecimalField(decimal_places=3, max_digits=50, default=0)


class MachineProcessStats(models.Model):
    datetime = models.DateTimeField(default=datetime.datetime.now())
    machine = models.ForeignKey(Machine)

    pid = models.IntegerField()
    name = models.CharField(max_length=100)
    user = models.CharField(max_length=100)

    cpu_usage = models.DecimalField(decimal_places=3, max_digits=10)
    mem_usage = models.DecimalField(decimal_places=3, max_digits=10)


log_types = (
    ('info', 'INFO'),
    ('error', 'ERROR'),
    ('warning', 'WARNING')
)


class MachineLog(models.Model):
    machine = models.ForeignKey(Machine, related_name="logs")
    datetime = models.DateTimeField()
    text = models.TextField()
    type = models.CharField(max_length=10, choices=log_types)

    def __unicode__(self):
        return "%s %s %s" % (self.machine, self.datetime, self.text)

