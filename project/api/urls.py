from django.conf.urls.defaults import *
from api.authentication import BackupBasicAPIAuthentication
from api.backupsapi.handlers import BackupHandler
from api.companiesapi.handlers import CompanyHandler
from api.machinesapi.handlers import MachineHandler, MachineLogHandler
from api.schedulesapi.handlers import SchedulesBackupHandler
from piston.resource import Resource

auth = BackupBasicAPIAuthentication()

companies = Resource(handler=CompanyHandler, authentication=None)
machine = Resource(handler=MachineHandler, authentication=None)
machinelog = Resource(handler=MachineLogHandler, authentication=None)
schedules = Resource(handler=SchedulesBackupHandler, authentication=None)
backups = Resource(handler=BackupHandler, authentication=None)

urlpatterns = patterns('',
                       #Companies
                       url(r'companies/$', companies),
                       url(r'companies/(?P<id>\d+)/$', companies),

                       #Machines
                       url(r'machines/$', machine),
                       url(r'machines/(?P<id>\w+)/$', machine),

                       #MachineLog
                       url(r'machinelogs/$', machinelog),
                       url(r'machinelogs/(?P<machine_id>\d+)/$', machinelog),
                       url(r'machinelogs/(?P<offset>\d+)/(?P<limit>\d+)/$', machinelog),
                       url(r'machinelogs/(?P<machine_id>\d+)/(?P<offset>\d+)/(?P<limit>\d+)/$', machinelog),

                       #ScheduleBackups
                       url(r'schedules/$', schedules),
                       url(r'schedules/(?P<id>\d+)/$', schedules),

                       #Backups
                       url(r'backups/$', backups),
                       url(r'backups/(?P<id>\d+)/$', backups),
                       )