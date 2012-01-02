from datetime import datetime, timedelta
from django.contrib.auth.models import User
from django.db import models

class Company(models.Model):
    name = models.CharField(max_length=150)
    users = models.ManyToManyField(User, related_name="companies")

    def __unicode__(self):
        return "Company: %s" % self.name


class Customer(models.Model):
    name = models.CharField(max_length=150)
    company = models.ForeignKey(Company, related_name="customers")

    def __unicode__(self):
        return "Customer: %s" % self.name


class Location(models.Model):
    name = models.CharField(max_length=150)
    customer = models.ForeignKey(Customer, related_name="locations")

    def __unicode__(self):
        return "Location: %s" % self.name

up_time_types = (
        ('up', 'UP'),
        ('down', 'DOWN')
    )

#Meant to be base for both MachinUptime and PINGuptime
class UptimeLogBase(models.Model):
    datetime = models.DateTimeField(auto_now=True)
    type = models.CharField(max_length=5, choices=up_time_types, default="up")

    def fire_warning(self):
        pass


class MachineUptimeLog(UptimeLogBase):
    machine = models.ForeignKey('Machine', related_name="updatelogs")

machine_timeout_minutes = 10 * 60

class Machine(models.Model):
    name = models.CharField(max_length=150)
    location = models.ForeignKey(Location, related_name="machines")
    machine_id = models.CharField(max_length=150)
    last_connection_to_client = models.DateTimeField(blank=True, null=True)
    ip = models.IPAddressField(null=True, blank=True)

    def __unicode__(self):
        return "Machine: %s, machine_id: %s" % (self.name, self.machine_id)

    @staticmethod
    def create_uptime_logs():
        for machine in Machine.objects.all():
            if (datetime.now() - machine.last_connection_to_client).seconds < machine_timeout_minutes:
                machine.create_uptime_log("up")
            else:
                machine.create_uptime_log("down")

    def set_last_connection_to_client(self):
        self.last_connection_to_client = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.save()

    def create_uptime_log(self, type):
        log = MachineUptimeLog()
        log.type = type
        log.machine = self
        log.save()

    def get_latest_stats(self):
        if self.stats.all().count() > 15:
            return self.stats.all().order_by("id")[self.stats.all().count()-16:]

        return self.stats.all().order_by("id")

    def get_latest_logs(self):
        return self.logs.all().order_by("-id")[0:50]

    def get_latest_backups(self):
        return self.backups.all().order_by("-id")[0:6]

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
        return self.running_restore() or self.running_backup()

    def get_last_backup_time(self):
        next_backup_time = None
        for schedule in self.schedules.all():
            if not next_backup_time:
                next_backup_time = schedule.get_last_backup_time()
            elif schedule.get_next_backup_time() > next_backup_time:
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
    datetime     = models.DateTimeField(default=datetime.now())
    machine      = models.ForeignKey(Machine, related_name="stats")

    load_average = models.DecimalField(decimal_places=3, max_digits=50)

    cpu_system   = models.DecimalField(decimal_places=3, max_digits=50)
    cpu_user     = models.DecimalField(decimal_places=3, max_digits=50)
    cpu_stolen   = models.DecimalField(decimal_places=3, max_digits=50)

    mem_used = models.IntegerField(default=0)
    mem_free = models.IntegerField(default=0)




class MachineProcessStats(models.Model):
    datetime     = models.DateTimeField(default=datetime.now())
    machine      = models.ForeignKey(Machine)

    pid          = models.IntegerField()
    name         = models.CharField(max_length=100)
    user         = models.CharField(max_length=100)

    cpu_usage    = models.DecimalField(decimal_places=3, max_digits=10)
    mem_usage    = models.DecimalField(decimal_places=3, max_digits=10)

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

storage_types = (
        ('ftp', 'FTP'),
        ('s3', 'Amazon S3')
    )

class Storage(models.Model):
    type = models.CharField(max_length=10, choices=storage_types)

    host = models.CharField(max_length=150)
    username = models.CharField(max_length=80)
    password = models.CharField(max_length=80)

    #FTP folder or S3 bucket
    folder = models.CharField(max_length=255)

    def __unicode__(self):
        return "Storage: %s %s" % (self.type, self.host)


class FolderBackup(models.Model):
    local_folder_path = models.TextField()
    schedule_backup = models.ForeignKey('ScheduleBackup', related_name='folder_backups')
    skip_hidden_folders = models.BooleanField(default=False)


    def __unicode__(self):
        return "%s" % self.schedule_backup

sql_types = (
        ('mysql', 'MySQL'),
        ('mssql', 'MSSQL')
    )

class SQLBackup(models.Model):
    type = models.CharField(max_length=40, choices=sql_types)
    schedule_backup = models.ForeignKey('ScheduleBackup', related_name='sql_backups')

    host = models.CharField(max_length=100)
    port = models.CharField(max_length=15)
    database = models.CharField(max_length=100)
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)

    def __unicode__(self):
        return "SQLBackup: %s" % self.host

class ScheduleBackup(models.Model):
    #Details
    machine = models.ForeignKey(Machine, related_name="schedules")
    name = models.CharField(max_length=150, blank=True)

    storage = models.ForeignKey(Storage, related_name="schedules")

    from_date = models.DateTimeField()
    last_run_time = models.DateTimeField()

    #Used to choose folder to save file
    current_version_in_loop = models.IntegerField(blank=True)
    versions_count = models.IntegerField()

    #Every x minute, perfrom backup
    repeat_every_minute = models.IntegerField()

    #Status messages to client
    running_backup = models.BooleanField(default=False, blank=True)
    running_restore = models.BooleanField(default=False, blank=True)

    active = models.BooleanField(default=True)

    def __unicode__(self):
       return u"Machine: %s, name: %s" % (self.machine, self.name)

    def current_day_folder_path(self):
        print

        if self.machine.last_connection_to_client.day != datetime.now().day:
            if self.current_version_in_loop < self.versions_count:
                self.current_version_in_loop += 1
            else:
                self.current_version_in_loop = 1

            self.save()

        return str(self.machine.machine_id) + "/" + "schedules/" + str(self.id) + "/" + str(
            self.current_version_in_loop) + "/"

    def get_last_backup(self):
        if self.backups.all().count() > 0:
            return self.backups.all()[self.backups.all().count() - 1]
        return None

    def get_last_backup_time(self):
        if self.get_last_backup():
            return self.get_last_backup().time_started
        return None

    def get_next_backup_time(self):
        if not self.get_last_backup():
            return self.from_date

        return self.get_last_backup_time() + timedelta(0, self.repeat_every_minute * 60)

class Backup(models.Model):
    machine = models.ForeignKey(Machine, related_name="backups")
    schedule = models.ForeignKey(ScheduleBackup, null=True, related_name="backups")
    time_started = models.DateTimeField()
    time_ended = models.DateTimeField(null=True, blank=True)
    day_folder_path = models.CharField(max_length=150, blank=True)

    def is_recoverable(self):
       return self.schedule.backups.filter(id__gt = self.id).count() < self.schedule.versions_count

    def save(self, *args, **kwargs):
        self.day_folder_path = self.schedule.current_day_folder_path()
        super(Backup, self).save(args, kwargs)