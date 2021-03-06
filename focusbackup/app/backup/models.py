# -*- coding: utf-8 -*-
import datetime
from dateutil.relativedelta import relativedelta, FR
from dateutil.rrule import rrule, MINUTELY
from django.db import models

from focusbackup.app.machine.models import Machine
from focusbackup.app.storage.models import Storage


schedule_every_minute_choices = (
    (5, 'Hvert 5 min'),
    (10, 'Hvert 10 min'),
    (15, 'Hvert kvarter'),
    (60, 'Hver time'),
    (180, 'Hver tredje time'),
    (1440, 'Hver dag'),
    (2880, 'Hver andre dag'),
    (4320, 'Hver tredje dag'),
    (10080, 'Hver uke'),
    (43829, 'Hver måned'),
)


class Schedule(models.Model):
    name = models.CharField(max_length=150)

    machine = models.ForeignKey(Machine, related_name="schedules")
    storage = models.ForeignKey(Storage, related_name="schedules")

    from_date = models.DateTimeField()
    last_run_time = models.DateTimeField(null=True, default=None)

    # Used to choose folder to save file
    current_version_in_loop = models.IntegerField(blank=True, default=1)
    versions_count = models.IntegerField(default=10, verbose_name="Number of copies")

    # Perform backup every x minute
    repeat_every_minute = models.IntegerField(default=360, choices=schedule_every_minute_choices)

    # Status messages for client
    running_backup = models.BooleanField(default=False, blank=True)
    running_restore = models.BooleanField(default=False, blank=True)

    run_now = models.BooleanField(default=False, blank=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ["name", "id"]

    def __unicode__(self):
        return u"Machine: %s, name: %s" % (self.machine, self.name)

    def current_day_folder_path(self):
        return str(self.machine.id) + "/" + "schedules/" + str(self.id) + "/" + str(
            self.current_version_in_loop) + "/"

    def set_last_run_time(self):
        self.last_run_time = datetime.datetime.now()
        self.save(update_fields=["last_run_time"])

    def is_delayed(self):
        delay_limit = datetime.datetime.now() - datetime.timedelta(minutes=30)
        return self.calculate_next_run_time() < delay_limit

    def get_recoverable_backups(self, limit=15):
        return self.backups.all() \
                   .select_related("schedule") \
                   .prefetch_related("schedule__folders", "schedule__sql_backups") \
                   .order_by("-id")[0:min(limit, self.versions_count)]

    def calculate_next_run_time(self):

        if self.last_run_time:
            start_date = self.from_date

            if self.repeat_every_minute < 9000:
                one_week_ago = datetime.datetime.now() - relativedelta(weeks=1)
                start_date = start_date.replace(one_week_ago.year,
                                                one_week_ago.month,
                                                one_week_ago.day)

            extra_days = (self.repeat_every_minute / 1400) + 10

            runs = list(rrule(MINUTELY,
                              cache=True,
                              interval=self.repeat_every_minute,
                              until=datetime.date.today() + relativedelta(days=extra_days,
                                                                          weekday=FR(-1)),

                              dtstart=start_date))

            for run in runs:
                if run > self.last_run_time:
                    return run

        return self.from_date

    def get_next_run_time(self):

        if self.run_now:
            return datetime.datetime.now() - datetime.timedelta(days=2)

        if self.repeat_every_minute == 0:
            return datetime.datetime.now() - datetime.timedelta(days=2)

        if self.is_delayed():
            return datetime.datetime.now() - datetime.timedelta(days=2)

        return self.calculate_next_run_time()

    def get_next_run_time_text(self):
        if self.get_next_run_time() < datetime.datetime.now():
            return "now"

        return self.get_next_run_time()

    def get_last_backup(self):
        if self.backups.all().count() > 0:
            return self.backups.all()[self.backups.all().count() - 1]
        return None

    def get_last_backup_time(self):
        if self.get_last_backup():
            return self.get_last_backup().time_started
        return None


class Backup(models.Model):
    machine = models.ForeignKey(Machine, related_name="backups")
    schedule = models.ForeignKey(Schedule, null=True, related_name="backups")
    time_started = models.DateTimeField()
    time_ended = models.DateTimeField(null=True, blank=True)
    day_folder_path = models.CharField(max_length=150, blank=True)
    file_name = models.CharField(max_length=150, blank=True, null=True)

    class Meta:
        ordering = ["-id"]

    def __unicode__(self):
        return u"Backup machine: %s, schedule: %s" % (self.machine, self.schedule)

    def recover_link(self):
        file_name = ""
        if self.schedule:
            if self.schedule.folders.all().count() + self.schedule.sql_backups.all().count() == 1:
                if len(self.file_name) > 0:
                    file_name = self.file_name.replace("C:", "")

        if self.day_folder_path:
            url = "ftp://%s:%s@%s/%s" % (
                self.schedule.storage.username, self.schedule.storage.password,
                self.schedule.storage.host,
                self.day_folder_path)

            return url + file_name
        return ""


class Folder(models.Model):
    schedule = models.ForeignKey(Schedule, null=True, related_name='folders')

    local_folder_path = models.TextField()
    skip_hidden_folders = models.BooleanField(default=False)

    class Meta:
        ordering = ["id"]

    def __unicode__(self):
        return u"Folder %s, schedule %s, machine %s" % (
            self.local_folder_path, self.schedule, self.schedule.machine)


sql_types = (
    ("", "Velg"),
    ('mysql', 'MySQL'),
    ('mssql', 'MSSQL')
)


class SQL(models.Model):
    schedule = models.ForeignKey(Schedule, related_name='sql_backups', null=True)
    type = models.CharField(max_length=40, choices=sql_types)

    host = models.TextField()
    port = models.TextField()
    database = models.TextField()
    username = models.TextField()
    password = models.TextField()

    class Meta:
        ordering = ["id"]

    def __unicode__(self):
        return "SQLBackup: %s" % self.host
