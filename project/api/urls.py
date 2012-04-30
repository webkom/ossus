from django.conf.urls.defaults import *
from api.authentication import BackupBasicAPIAuthentication
from api.backupsapi.handlers import BackupHandler
from api.clientversions.handlers import ClientVersionHandler
from api.companiesapi.handlers import CompanyHandler
from api.machinesapi.handlers import MachineHandler, MachineLogHandler, MachineStatsHandler
from api.schedulesapi.handlers import SchedulesBackupHandler
from api.tokenauthentication import TokenAPIAuthentication
from piston.resource import Resource

class CsrfExemptResource(Resource):
    """A Custom Resource that is csrf exempt"""
    def __init__(self, handler, authentication=None):
        super(CsrfExemptResource, self).__init__(handler, authentication)
        self.csrf_exempt = getattr(self.handler, 'csrf_exempt', True)

auth = TokenAPIAuthentication()

companies = CsrfExemptResource(handler=CompanyHandler, authentication=auth)
machine = CsrfExemptResource(handler=MachineHandler, authentication=auth)
machinelog = CsrfExemptResource(handler=MachineLogHandler, authentication=auth)
machinestats = CsrfExemptResource(handler=MachineStatsHandler, authentication=auth)
schedules = CsrfExemptResource(handler=SchedulesBackupHandler, authentication=auth)
backups = CsrfExemptResource(handler=BackupHandler, authentication=auth)
clientversion = CsrfExemptResource(handler=ClientVersionHandler, authentication=auth)


urlpatterns = patterns('',
    #Companies
    url(r'^companies/$', companies),
    url(r'^companies/(?P<id>\d+)/$', companies),

    #Machines
    url(r'^machines/$', machine),
    url(r'^machines/(?P<id>\w+)/$', machine),

    #Used for updating version
    url(r'^machines/(?P<id>\w+)/set_agent_version/(?P<agent_version_id>\w+)$', machine),
    url(r'^machines/(?P<id>\w+)/set_updater_version/(?P<updater_version_id>\w+)$', machine),

    #MachineLog
    url(r'^machinelogs/$', machinelog),
    url(r'^machinelogs/(?P<machine_id>\d+)/$', machinelog),
    url(r'^machinelogs/(?P<offset>\d+)/(?P<limit>\d+)/$', machinelog),
    url(r'^machinelogs/(?P<machine_id>\d+)/(?P<offset>\d+)/(?P<limit>\d+)/$', machinelog),

    #MachineStats
    url(r'^machinestats/$', machinestats),

    url(r'^machinestats/(?P<machine_id>\d+)/$', machinestats),

    #ScheduleBackups
    url(r'^schedules/$', schedules),
    url(r'^schedules/(?P<id>\d+)/$', schedules),

    url(r'^machines/(?P<machine_id>\d+)/schedules/$', schedules),

    #Backups
    url(r'^backups/$', backups),
    url(r'^backups/(?P<id>\d+)/$', backups),

    #Client versions
    url(r'^clientversions/$', clientversion),
    url(r'^clientversions/(?P<name>[A-Za-z\.0-9]+)/$', clientversion),

    url(r'^clientversions/current_agent/$', clientversion, {'current_agent': True}),
    url(r'^clientversions/current_updater/$', clientversion, {'current_updater':True}),

)
