import os
import sys

from django.conf import settings
from django_fabric import App

from fabric.decorators import task
from fabric.operations import put
from fabric.state import env

sys.path.append(os.path.dirname(__file__))

env.user = 'focus'
env.hosts = ['kontor.focussecurity.no']

site = App(
    project_paths={
        'prod': '/opt/web/focus24.no/focusbackup/',
    },
    project_package='focusbackup',
    test_settings='focusbackup.settings.test',
    restart_command='/etc/init.d/supervisord restart',
    local_tables_to_flush=[],
    requirements={
        'prod': 'requirements.txt',
    }
)

@task
def deploy():
    site.deploy('prod')

@task
def upload_client():

    #Upload Agent
    put("%s%s" % (settings.PATH_LOCAL_FOCUSBACKUPCLIENT, "Agent_jar/Agent.jar"), "/tmp/Agent.jar")
    put("%s%s" % (settings.PATH_LOCAL_FOCUSBACKUPCLIENT, "Updater_jar/Updater.jar"), "/tmp/Update.jar")
    put("%s%s" % (settings.PATH_LOCAL_FOCUSBACKUPCLIENT, "setup_jar/setup.jar"), "/tmp/installer.jar")


@task
def clone_prod_data():
    site.clone_data('prod')
