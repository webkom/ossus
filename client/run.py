from models import Machine
import os

BASE_PATH = os.path.dirname(__file__)

if BASE_PATH:
    BASE_PATH+=os.sep

try:
    f = open(BASE_PATH+"settings.txt", "r")
except Exception, e:
    print "ERROR: Finner ikke settings.txt"
    exit()

settings_dict = {}

for line in f.readlines():
    try:
        key, value = line.split(":")
        settings_dict[key.strip()] = value.strip()
    except Exception, e:
        print e
        exit()

machine = Machine(settings_dict)
machine.run_backup()