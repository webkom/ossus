from django.conf.urls.defaults import *
from api.authentication import BackupBasicAPIAuthentication
from api.backupsapi.handlers import BackupHandler
from api.clientversions.handlers import ClientVersionHandler
from api.companiesapi.handlers import CompanyHandler
from api.machinesapi.handlers import MachineHandler, MachineLogHandler, MachineStatsHandler
from api.schedulesapi.handlers import SchedulesBackupHandler
from piston.resource import Resource

auth = BackupBasicAPIAuthentication()

companies = Resource(handler=CompanyHandler, authentication=auth)
machine = Resource(handler=MachineHandler, authentication=auth)
machinelog = Resource(handler=MachineLogHandler, authentication=auth)
machinestats = Resource(handler=MachineStatsHandler, authentication=auth)
schedules = Resource(handler=SchedulesBackupHandler, authentication=auth)
backups = Resource(handler=BackupHandler, authentication=auth)
clientversion = Resource(handler=ClientVersionHandler, authentication=auth)

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

    #MachineStats
    url(r'machinestats/$', machinestats),
    url(r'machinestats/(?P<machine_id>\d+)/$', machinestats),

    #ScheduleBackups
    url(r'schedules/$', schedules),
    url(r'schedules/(?P<id>\d+)/$', schedules),

    #Backups
    url(r'backups/$', backups),
    url(r'backups/(?P<id>\d+)/$', backups),

    #Client versions
    url(r'clientversions/$', clientversion),
    url(r'clientversions/(?P<name>[A-Za-z\.0-9]+)/$', clientversion),

    url(r'clientversions/current_agent/$', clientversion, {'current_agent': True}),
    url(r'clientversions/current_updater/$', clientversion, {'current_updater':True}),

)
