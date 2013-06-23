#!/bin/bash

ssh web@'kontor.focussecurity.no' '
    cd /opt/web/focus24.no/focusbackup
    git pull origin master
    source venv/bin/activate
    python manage.py syncdb --migrate
'
