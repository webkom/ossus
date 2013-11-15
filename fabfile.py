import os
from fabric.contrib.console import confirm
from fabric.decorators import task
from fabric.state import env
from django_fabric import App
import sys

sys.path.append(os.path.dirname(__file__))

env.user = 'focus'
env.hosts = ['kontor.focussecurity.no']

site = App(
    project_paths={
        'focus': '/opt/web/focus24.no/focusbackup',
    },
    project_package='focusbackup',
    test_settings='focusbackup.settings.test',
    restart_command='/etc/init.d/supervisord restart',
    requirements={
        'focus': 'requirements.txt',
    }
)


@task
def deploy():
    site.deploy('focus')