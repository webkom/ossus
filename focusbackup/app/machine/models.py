# -*- coding: utf-8 -*-
from copy import deepcopy
import datetime

from django.db import models, transaction, IntegrityError

from focusbackup.app.client.models import ClientVersion
from focusbackup.app.customer.models import Customer
from focusbackup.app.machine.managers import LockingManager


class Machine(models.Model):
    name = models.CharField(max_length=150)
    customer = models.ForeignKey(Customer, related_name="machines")
    run_install = models.BooleanField(default=True)

    active = models.BooleanField(default=True)
    template = models.BooleanField(default=False)

    #Info from the client
    last_connection_to_client = models.DateTimeField(blank=True, null=True,
                                                     default=datetime.datetime.now())

    external_ip = models.IPAddressField(default="")

    #For generating settings-file
    local_temp_folder = models.CharField(max_length=255, default="C:\\focus24\\temp\\")
    agent_folder = models.CharField(max_length=255, default="C:\\focus24\\")
    mysql_dump = models.CharField(max_length=255, default="mysqldump")

    auto_version = models.BooleanField(default=True)

    lock = models.DateTimeField(default=None, null=True, blank=True)
    lock_session = models.CharField(max_length=255, null=True, default=None)

    #Current version running on client
    current_agent_version = models.ForeignKey(ClientVersion, related_name="agent_versions",
                                              null=True)
    current_updater_version = models.ForeignKey(ClientVersion, related_name="updater_versions",
                                                null=True)

    #If not auto_version
    selected_agent_version = models.ForeignKey(ClientVersion, related_name="agent_selected",
                                               null=True, blank=True)
    selected_updater_version = models.ForeignKey(ClientVersion, related_name="updater_selected",
                                                 null=True, blank=True)

    class Meta:
        ordering = ["-active", "name", "id"]

    def __unicode__(self):
        return "Machine: %s, id: %s" % (self.name, self.id)

    def set_lock(self, session=None):
        try:
            with transaction.atomic():
                self.lock = datetime.datetime.now()
                self.lock_session = session
                self.save()
                self.log("info", "lock set by %s" % session)
        except IntegrityError:
            self.log("error", "error locking..")

    def release_lock(self, session=None):
        try:
            with transaction.atomic():
                last_locked_date = self.lock
                self.lock = None
                self.lock_session = None
                self.save()
                self.log("info", "lock (from %s) released by %s" % (last_locked_date, session))
        except IntegrityError:
            self.log("error", "error unlocking..")

    def clone(self):
        copy = deepcopy(self)
        copy.pk = None
        copy.template = False
        copy.save()

        for schedule in self.schedules.all():
            schedule_copy = deepcopy(schedule)
            schedule_copy.pk = None
            schedule_copy.machine = copy
            schedule_copy.save()

            for folder in schedule.folders.all():
                folder_copy = deepcopy(folder)
                folder_copy.pk = None
                folder_copy.schedule = schedule_copy
                folder_copy.save()

            for sql in schedule.sql_backups.all():
                sql_copy = deepcopy(sql)
                sql_copy.pk = None
                sql_copy.schedule = schedule_copy
                sql_copy.save()

        return copy

    def is_up_to_date(self):
        return self.current_agent_version.current_agent and self.current_updater_version.current_updater

    def lost_connection_to_client(self):
        return datetime.datetime.now() - self.last_connection_to_client > datetime.timedelta(
            minutes=20)

    def set_last_connection_to_client(self):
        self.last_connection_to_client = datetime.datetime.now()
        self.active = True
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
        return self.stats.all()[0:20]

    def get_latest_logs(self):
        return self.logs.all().order_by("-id")[0:8]

    def log(self, log_type, text):
        machine_log = MachineLog(machine=self,
                                 datetime=datetime.datetime.now(),
                                 type=log_type,
                                 text=text)

        machine_log.save()

    def delayed_schedules(self):
        schedules = []

        for schedule in self.schedules.all():
            if schedule.is_delayed():
                schedules.append(schedule.id)

        return self.schedules.filter(id__in=schedules)

    def get_latest_backups(self):
        return self.backups.select_related("schedule").prefetch_related("schedule__folders", "schedule__sql_backups").order_by("-id")[0:8]

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
        return self.running_restore() or self.running_backup() or self.lock is not None

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

    class Meta:
        ordering = ['-id']


class MachineProcessStats(models.Model):
    datetime = models.DateTimeField(default=datetime.datetime.now())
    machine = models.ForeignKey(Machine)

    pid = models.IntegerField()
    name = models.CharField(max_length=100)
    user = models.CharField(max_length=100)

    cpu_usage = models.DecimalField(decimal_places=3, max_digits=10)
    mem_usage = models.DecimalField(decimal_places=3, max_digits=10)

    class Meta:
        ordering = ['-id']

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

    class Meta:
        ordering = ["-id"]

    def __unicode__(self):
        return "%s %s %s" % (self.machine, self.datetime, self.text)