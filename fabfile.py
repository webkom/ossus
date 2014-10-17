import os
import sys

from django.conf import settings
from django_fabric import App

from fabric.context_managers import cd
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
    dumpdata_command="dumpdata "
                     "--exclude machine.MachineStats "
                     "--exclude machine.MachineProcessStats "
                     "--exclude machine.MachineLog "
                     "--exclude backup.Backup",
    requirements={
        'prod': 'requirements.txt',
    }
)


@task
def deploy():
    site.deploy('prod')


@task
def upload_client():
    # Upload Agent
    put("%s%s" % (settings.PATH_LOCAL_FOCUSBACKUPCLIENT,
                  "Agent_jar/Agent.jar"), "/tmp/Agent.jar")

    put("%s%s" % (settings.PATH_LOCAL_FOCUSBACKUPCLIENT,
                  "Updater_jar/Updater.jar"), "/tmp/Updater.jar")

    put("%s%s" % (settings.PATH_LOCAL_FOCUSBACKUPCLIENT,
                  "setup_jar/setup.jar"), "/tmp/installer.jar")

    with cd(site.project_paths['prod']):
        site.run_management_command('prod', "set_new_client")


@task
def clone_prod_data():
    # Empty local database before doing anything
    from django.db import connection

    cursor = connection.cursor()
    cursor.execute("DROP DATABASE focus24;")
    cursor.execute("CREATE DATABASE focus24;")

    # from django import db
    # db.close_connection()
    cursor.execute("USE focus24;")

    site.clone_data('prod')
