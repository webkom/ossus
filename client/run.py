from models import Machine

settings_dict = {
    'server_ip': "backup.fncit.no",
    'machine_id': "1001",
    'username': '',
    'password': '',
    'os_system': '',
    'force_action': False,
    }

machine = Machine(settings_dict)
for schedule in machine.schedules:
    schedule.run()