#!/bin/bash
set -e # Exit on error


ssh focus@kontor.focussecurity.no'
    ssh 'focus'@'10.0.6.31' "
        cd /var/webapps/focus24/focusbackup
        git pull origin master
        bin/django syncdb
        bin/django migrate --merge
        sudo /etc/init.d/httpd restart
    "
'