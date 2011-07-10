# -*- coding: utf-8 -*-
import ftplib
import os
from backup_system import restore_backup_from_ftp
from backup_system import run_check
from client.backup_system import write_log

settings = {
    'server_ip': "localhost:8000",
    'machine_id': "734865",
    'username': '',
    'password': '',
    'os': '',
    'force_action': True,
}

write_log(settings, "info", "Backup initialized")

try:
    run_check(settings)
except Exception, e:
    write_log(settings,"error", str(e))

write_log(settings, "info", "Backup initialized")

