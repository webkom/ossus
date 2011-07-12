# -*- coding: utf-8 -*-
import base64
import ftplib
from poster.encode import multipart_encode
from poster.streaminghttp import register_openers
from datetime import datetime
import os
import urllib2
import simplejson

log_file_path = "log.txt"
base_api_path = "http://"
machines_api_path = "/api/machines/"
machine_logs_api_path = "/api/machinelogs/"

def post_data_to_api(post_url, data_dict, username, password):
    register_openers()
    datagen, headers = multipart_encode(data_dict)
    request = urllib2.Request(post_url, datagen, headers)
    base64string = base64.encodestring('%s:%s' % (username, password)).replace('\n', '')
    request.add_header("Authorization", "Basic %s" % base64string)
    return urllib2.urlopen(request).read()
    
def download_data_from_api(theurl, username, password):
    passman = urllib2.HTTPPasswordMgrWithDefaultRealm()
    passman.add_password(None, theurl, username, password)
    authhandler = urllib2.HTTPBasicAuthHandler(passman)
    opener = urllib2.build_opener(authhandler)
    urllib2.install_opener(opener)
    pagehandle = urllib2.urlopen(theurl)
    return simplejson.loads(pagehandle.read())

class Log:

    def __init__(self, machine, type, text):
        self.log_file_path = log_file_path
        self.machine = machine
        self.type = type
        self.text = text

        self.add_line_to_top_of_log()
        self.save_log_to_server()


    def add_line_to_top_of_log(self):
        self.create_log_file_if_not_created()
        old_content = self.read_log()

        file = open(self.log_file_path, "w")
        file.write(self.create_log_message())
        file.write(old_content)
        file.close()

    def read_log(self):
        self.create_log_file_if_not_created()
        file = open(self.log_file_path, "r")
        text = file.read()
        file.close()
        return text

    def save_log_to_server(self):
        self.create_log_file_if_not_created()
        post_url = "%s%s%s/" % (base_api_path, self.machine.server_ip, machine_logs_api_path)

        data_dict = {
            'machine_id': self.machine.machine_id,
            'text': self.text,
            'type': self.type,
            'datetime': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        post_data_to_api(post_url, data_dict, self.machine.username, self.machine.password)

    def create_log_message(self):
        return "[" + str(self.type).upper() + "] " + str(datetime.now()) + " %s \n" % self.text

    def create_log_file_if_not_created(self):
        if not os.path.exists(self.log_file_path):
            open(self.log_file_path, "w")


class Machine:
    def __init__(self, settings_dict):
        self.server_ip = settings_dict['server_ip']
        self.machine_id = settings_dict['machine_id']
        self.username = settings_dict['username']
        self.password = settings_dict['password']
        self.os_system = settings_dict['os_system']
        self.force_action = settings_dict['force_action']

        machine_data = self.get_machine_data_from_api()

        self.id = machine_data['id']
        self.is_busy = machine_data['is_busy']

        self.add_schedules(machine_data['schedules'])

    def get_machine_data_from_api(self):
        url = "%s%s%s%s/" % (base_api_path, self.server_ip, machines_api_path, self.machine_id)
        return download_data_from_api(url, self.username, self.password)

    def log_info(self, text):
        Log(self, "info", text)

    def log_error(self, text):
        Log(self, "error", text)

    def add_schedules(self, schedules):
        self.schedules = []
        for schedule in schedules:
            self.schedules.append(Schedule(self, schedule))

class FTPStorage:
    def __init__(self, schedule, ip, username, password, folder):
        self.connection = ftplib.FTP(ip, username, password)
        self.folder = folder
        self.schedule = schedule

    def upload_file_to_folder(self, local_file_path, file_name, storage_folder):
        f = open(local_file_path, "rb")
        self.connection.cwd("~/")
        self.connection.storbinary("STOR %s%s" % (storage_folder, file_name), f, 1024)
        self.connection.cwd("~/")
        f.close()
                
class S3Storage:
    def __init__(self, schedule, username, password, folder):
        raise NotImplementedError, "S3 not implemented yet"

class Storage:
    def __init__(self, schedule, storage_dict):
        self.schedule = schedule
        self.type = storage_dict['type']
        self.host = storage_dict['host']
        self.username = storage_dict['username']
        self.password = storage_dict['password']
        self.folder = storage_dict['folder']

        self.set_correct_backend()

    def upload_file_to_folder(self, local_file_path, file_name, storage_folder):
        self.backend.upload_file_to_folder(local_file_path, file_name, storage_folder)

    def set_correct_backend(self):
        if self.type.upper() == "FTP":
            self.backend = FTPStorage(self.schedule, self.host, self.username, self.password, self.folder)
            return self.backend
        if self.type.upper() == "S3":
            self.backend = S3Storage(self.schedule, self.username, self.password, self.folder)
            return self.backend
        
        raise Exception, "No backend selected, you have to use FTP or S3"
            
class Schedule:
    def __init__(self, machine, schedule_dict):
        self.machine = machine

        self.id = schedule_dict['id']
        self.name = schedule_dict['name']

        self.storage = Storage(self, schedule_dict['storage'])

        self.next_backup_time = datetime.strptime(schedule_dict['get_next_backup_time'], "%Y-%m-%d %H:%M:%S")

    def run(self):
        if not self.schedule_should_run():
            self.machine.log_info("Waiting, %s will not run before %s" % (self, str(self.next_backup_time)))
            return

        self.machine.log_info("Starting schedule %s" % self)
        
    def schedule_should_run(self):
        return datetime.now() > self.next_backup_time or machine.force_action

    def  __repr__(self):
        return "Schedule %s, %s" % (self.id, self.name)


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