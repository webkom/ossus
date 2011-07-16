# -*- coding: utf-8 -*-
import base64
import ftplib
import shutil
import zipfile
from poster.encode import multipart_encode
from poster.streaminghttp import register_openers
from datetime import datetime
import os
import urllib2
import simplejson


log_file_path = "log_backup.txt"
base_api_path = "http://"

#APIpaths
schedule_api_path = "/api/schedules/"
machines_api_path = "/api/machines/"
machine_logs_api_path = "/api/machinelogs/"

#Local paths
BASE_PATH = os.path.dirname(__file__)+os.sep
mysql_dump = "mysqldump5"
temp_folder = BASE_PATH + "temps" + os.sep
database_backup_folder = BASE_PATH + "sql_backup" + os.sep

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
        self.force_action = False

        if settings_dict['force_action'] == '1':
            self.force_action = False

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

    def log_warning(self, text):
        Log(self, "warning", text)

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
        self.connection.cwd("~/")
        f = open(local_file_path, "rb")
        store_path = "~/" + storage_folder + file_name
        self.connection.storbinary("STOR %s" % store_path, f, 1024)
        self.connection.cwd("~/")
        f.close()

    def folder_exists_in_current_directory(self, folder):
        filelist = []
        self.connection.retrlines('LIST', filelist.append)

        for f in filelist:
            folder_name = f.split()[8]
            for o in f.split()[9:]:
                folder_name += " " + o

            if folder_name == folder:
                return True

        return False

    def folder_path_exists(self, folder):

        for folder_part in folder.split("/"):
            if folder_part == "" or folder_part == "~":
                continue

            if self.folder_exists_in_current_directory(folder_part):
                self.connection.cwd(folder_part)
            else:
                return False

        return True

    def create_folder(self, ftp_folder):

        ftp_folder = ftp_folder
        if self.folder_path_exists(ftp_folder):
            return False

        self.connection.cwd("~/")
        for folder in ftp_folder.split("/"):
            if folder == "":
                continue

            if self.folder_exists_in_current_directory(folder):
                self.connection.cwd(folder)
            else:
                self.connection.mkd(folder)
                self.connection.cwd(folder)

        return True

    def delete_folder(self, folder):
        folder = "~/" + folder

        if not self.folder_path_exists(folder):
            self.schedule.machine.log_info(
                "Tried to delete folder %s from ftp storage %s, but the folder does not exist" % (
                    folder, self.connection.host))
            return False

        self.schedule.machine.log_info("Deleting folder %s from ftp storage %s" % (folder, self.connection.host))

        for file in self.connection.nlst(folder):
            if file == '.' or file == '..':
                continue

            if os.path.splitext(str(file))[1]:
                self.connection.delete("%s" % file)
            else:
                self.delete_folder(folder)

        self.connection.rmd(folder)
        return True


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

    def save_folder_as_zip(self, folder_to_zip, save_as):
        zipf = zipfile.ZipFile(str(save_as), mode="w")
        self.create_zip(zipf, folder_to_zip)
        zipf.close()

        return zipf

    def create_zip(self, zipf, directory, folder=""):
        for item in os.listdir(directory):
            try:
                if os.path.isfile(os.path.join(directory, item)):
                    zipf.write(os.path.join(directory, item), folder + os.sep + item)
                elif os.path.isdir(os.path.join(directory, item)):
                    self.create_zip(zipf, os.path.join(directory, item), folder + os.sep + item)
            except Exception, e:
                self.schedule.machine.log_warning(str(e))

    def upload_folder(self, folder, save_in_folder):
        filename = self.create_filename_for_folder(folder)

        if not os.path.isdir(temp_folder):
            os.makedirs(temp_folder)
        
        zip_to_upload = self.save_folder_as_zip(folder, temp_folder + filename)
        self.upload_file(zip_to_upload.filename, filename, save_in_folder)
        return True

    def create_filename_for_folder(self, path_to_folder):
        ext = os.path.splitext(path_to_folder)[1]
        file_name = ""
        for f in os.path.splitext(path_to_folder)[0].split(os.sep):
            if f:
                file_name += f.lower() + "_"
            file_name += ext
        return file_name[:-1] + ".zip"

    def upload_file(self, local_file_path, file_name, storage_folder):
        self.backend.upload_file_to_folder(local_file_path, file_name, storage_folder)

    def folder_path_exists(self, folder_path):
        return self.backend.folder_path_exists(folder_path)

    def create_folder(self, folder):
        return self.backend.create_folder(folder)

    def delete_folder(self, folder):
        return self.backend.delete_folder(folder)

    def set_correct_backend(self):
        if self.type.upper() == "FTP":
            self.backend = FTPStorage(self.schedule, self.host, self.username, self.password, self.folder)
            return self.backend
        if self.type.upper() == "S3":
            self.backend = S3Storage(self.schedule, self.username, self.password, self.folder)
            return self.backend

        raise Exception, "No backend selected, you have to use FTP or S3"


class FolderBackup:
    def __init__(self, schedule, local_folder_path):
        self.schedule = schedule
        self.local_folder_path = local_folder_path

    def __repr__(self):
        return "FolderBackup %s " % self.local_folder_path

    def run(self):
        try:
            self.schedule.storage.upload_folder(self.local_folder_path, self.schedule.upload_path)
            self.schedule.machine.log_info("Backup of %s folder complete" % self.local_folder_path)
        except Exception, e:
            self.schedule.machine.log_error("Backup of %s folder failed" % self.local_folder_path)
            
class SQLBackup:
    def __init__(self, schedule, sql_dict):
        self.schedule = schedule
        self.type = sql_dict['type']
        self.host = sql_dict['host']
        self.database = sql_dict['database']
        self.username = sql_dict['username']
        self.password = sql_dict['password']

    def __repr__(self):
        return "SQLBackup %s " % self.database

    def run(self):
        self.prepare_local_sql_temps_folder_for_this_backup()

        if self.type.lower() == "mssql":
            self.backup_mssql()
        elif self.type.lower() == "mysql":
            self.backup_myssql()

        return False

    def prepare_local_sql_temps_folder_for_this_backup(self):
        if os.path.isdir(database_backup_folder):
            shutil.rmtree(database_backup_folder)
        os.makedirs(database_backup_folder+"/"+self.database)

    def backup_myssql(self):
        import subprocess

        try:
            output_dir = database_backup_folder+os.sep+self.database+os.sep
            output_file = "%s.sql" % self.database
            command = mysql_dump + " --host %s " % self.host + "--user " + self.username + " --password=" + self.password + " --add-locks --flush-privileges --add-drop-table --complete-insert --extended-insert --single-transaction --database " + self.database + " > " + output_dir + output_file
            subprocess.call(command, shell=True)
            self.schedule.storage.upload_folder(output_dir, self.schedule.upload_path)
            self.schedule.machine.log_info("Backup of %s database complete" % self.database)
        except Exception, e:
            self.schedule.machine.log_error(str(e))
            return False

        return True

    def backup_mssql(self):
        try:
            import pyodbc

            database_backup_file = database_backup_folder + "%s.bak" % self.database

            cnxn = pyodbc.connect('DRIVER={SQL Server};SERVER=%s;DATABASE=%s;UID=%s;PWD=%s' % (
                self.host, self.database, self.username, self.password))
            cnxn.autocommit = True
            cur = cnxn.cursor()

            cur.execute('BACKUP DATABASE ? TO DISK=?', [r'%s' % self.database, r'%s' % database_backup_file])

            while cur.nextset():
                pass

            self.schedule.storage.upload_folder(database_backup_folder, self.schedule.upload_path)

        except Exception, e:
            self.schedule.machine.log_error(str(e))
            return False

        self.schedule.machine.log_info("Backup of %s database complete" % self.database)

        return True


class Schedule:
    def __init__(self, machine, schedule_dict):
        self.machine = machine

        self.id = schedule_dict['id']
        self.name = schedule_dict['name']
        self.running_backup = schedule_dict['running_backup']
        self.running_restore = schedule_dict['running_restore']
        self.current_version_in_loop = schedule_dict['current_version_in_loop']
        self.versions_count = schedule_dict['versions_count']

        self.storage = Storage(self, schedule_dict['storage'])

        self.upload_path = self.storage.folder + schedule_dict['current_day_folder_path']

        self.add_folder_backups(schedule_dict['folder_backups'])
        self.add_sql_backups(schedule_dict['sql_backups'])

        self.next_backup_time = datetime.strptime(schedule_dict['get_next_backup_time'], "%Y-%m-%d %H:%M:%S")

    def run(self):
        if not self.schedule_should_run():
            self.machine.log_info("Waiting, %s will not run before %s" % (self, str(self.next_backup_time)))
            return

        self.clear_destination_folder_before_run()
        self.machine.log_info("Starting schedule %s" % self)

        for folder_backup in self.folder_backups:
            folder_backup.run()

        for sql_backup in self.sql_backups:
            sql_backup.run()

        self.increase_counter()

        self.machine.log_info("Schedule %s complete" % self)
        

    def clear_destination_folder_before_run(self):
        self.storage.delete_folder(self.upload_path)
        self.storage.create_folder(self.upload_path)

    def schedule_should_run(self):
        return datetime.now() > self.next_backup_time or machine.force_action

    def add_folder_backups(self, folder_backups):
        self.folder_backups = []
        for folder_backup in folder_backups:
            self.folder_backups.append(FolderBackup(self, folder_backup['local_folder_path']))

    def add_sql_backups(self, sql_backups):
        self.sql_backups = []
        for sql_backup in sql_backups:
            self.sql_backups.append(SQLBackup(self, sql_backup))

    def increase_counter(self):
        post_url = "%s%s%s%s/" % (base_api_path, self.machine.server_ip, schedule_api_path, self.id)

        data_dict = {
            'name': self.name,
            'machine_id': self.machine.machine_id,
            'running_backup': self.running_backup,
            'running_restore': self.running_restore,
            'current_version_in_loop': self.find_next_counter(),
            }

        post_data_to_api(post_url, data_dict, self.machine.username, self.machine.password)

    def find_next_counter(self):
        if self.current_version_in_loop >= self.versions_count:
            return 1
        return self.current_version_in_loop + 1

    def  __repr__(self):
        return "Schedule %s, %s" % (self.id, self.name)