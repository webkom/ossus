from models import Machine

try:
    f = open("settings.txt", "r")
except Exception, e:
    print "ERROR: Finner ikke settings.txt"
    exit()

settings_dict = {}

for line in f.readlines():
    key, value = line.split(":")

    settings_dict[key.strip()] = value.strip()

machine = Machine(settings_dict)
for schedule in machine.schedules:
    schedule.run()