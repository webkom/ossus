#!/bin/bash

ssh focus@'kontor.focussecurity.no' '
    cd /var/webapps/focus24/focusbackup
    git pull origin master
    bin/django syncdb
    bin/django migrate --merge
    sudo /etc/init.d/httpd restart
'
