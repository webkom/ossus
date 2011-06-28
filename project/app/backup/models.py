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

class Machine(models.Model):
    name = models.CharField(max_length=150)
    location = models.ForeignKey(Location, related_name="machines")
    machine_id = models.CharField(max_length=150)
    last_connection_to_client = models.DateTimeField(blank=True)
    ip = models.IPAddressField()

    def __unicode__(self):
        return "Machine: %s, machine_id: %s" % (self.name, self.machine_id)

    def set_last_connection_to_client(self):
        self.last_connection_to_client = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.save()

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

class FolderTask(models.Model):
    local_folder_path = models.TextField()
    schedule_backup = models.ForeignKey('ScheduleBackup', related_name='folder_tasks')

class ScheduleBackup(models.Model):

    #Details
    machine = models.ForeignKey(Machine, related_name="schedules")
    name = models.CharField(max_length=150, blank=True)
    from_date = models.DateTimeField()

    #Used to choose folder to save file
    current_day_in_loop = models.IntegerField()
    days_to_keep_backups = models.IntegerField()
    last_run_time = models.DateTimeField()

    #Ftp connection
    ftp_host = models.CharField(max_length=150)
    ftp_username = models.CharField(max_length=80)
    ftp_password = models.CharField(max_length=80)
    ftp_folder = models.CharField(max_length=255)
    
    #Every x minute, perfrom backup
    repeat_every_minute = models.IntegerField()

    #Status messages to client
    running_backup = models.BooleanField(default=False, blank=True)
    running_restore = models.BooleanField(default=False, blank=True)

    def current_day_folder_path(self):

        if self.machine.last_connection_to_client.day != datetime.now().day:
            if self.current_day_in_loop < self.days_to_keep_backups:
                self.current_day_in_loop +=1
            else:
                self.current_day_in_loop = 1
                
            self.save()
            
        return str(self.machine.machine_id) + "/" + str(self.current_day_in_loop) + "/"

    def get_last_backup(self):
        if self.backups.all().count()>0:
            return self.backups.all()[self.backups.all().count()-1]
        return None

    def get_last_backup_time(self):
        if self.get_last_backup():
            return self.get_last_backup().time_started
        return None

    def get_next_backup_time(self):
        if not self.get_last_backup():
            return self.from_date
        
        return self.get_last_backup_time()+timedelta(0,self.repeat_every_minute*60)

class Backup(models.Model):
    machine = models.ForeignKey(Machine, related_name="backups")
    schedule = models.ForeignKey(ScheduleBackup, null=True, related_name="backups")
    time_started = models.DateTimeField()
    day_folder_path = models.CharField(max_length=150, blank=True)

    def save(self, *args, **kwargs):
        self.day_folder_path = self.schedule.current_day_folder_path()
        super(Backup, self).save(args, kwargs)