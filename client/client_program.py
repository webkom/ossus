# -*- coding: utf-8 -*-
from backup_system import run_check,write_log

settings = {
    'server_ip': "192.168.1.211:8000",
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

write_log(settings, "info", "Backup completed")

