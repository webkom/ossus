# -*- coding: utf-8 -*-
import ftplib
from backup_system import run_check,write_log,restore_backup_from_ftp

settings = {
    'server_ip': "backup.fncit.no",
    'machine_id': "1001",
    'username': '',
    'password': '',
    'os': '',
    'force_action': True,
}

write_log(settings, "info", "Backup initialized")

try:
    run_check(settings)
    #restore_backup_from_ftp(93, settings)
except Exception, e:
    write_log(settings,"error", str(e))