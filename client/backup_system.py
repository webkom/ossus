# -*- coding: utf-8 -*-
import base64
from datetime import datetime
import ftplib
import shutil
import urllib2
import zipfile
import time
import simplejson
from poster.encode import multipart_encode
from poster.streaminghttp import register_openers
import os

"""

TODO
BACKUP MSSQL
http://ryepup.unwashedmeme.com/blog/2010/08/26/making-sql-server-backups-using-python-and-pyodbc/
http://www.cubicweb.org/blogentry/626769

CYCLES, days, unlimited? Hvis en skal ta vare på flere backups (1, hver mnd feks), så lager man 2 rutiner (schedules)

"""

"""
DO NOT CHANGE ANYTHING BELOW
"""

def write_log(settings,type, text):

    if not os.path.exists("log.txt"):
        open("log.txt","w")

    #read old content
    log_file = open("log.txt","r")
    log_file_content = log_file.read()

    #write new content
    log_file = open("log.txt","w")
    log_file.write("["+str(type).upper()+"] " + str(datetime.now()) + " %s \n" % text)
    log_file.write(log_file_content)
    log_file.close()

    #Save log to server
    theurl = "http://%s/api/machinelogs/" % settings['server_ip']

    machinelog_dict = {'machine_id': settings['machine_id'],
                       'text':text,
                       'type':type,
                       'datetime': datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

    set_data(theurl, machinelog_dict, settings)

def run_check(settings):

    machine = download_content("http://%s/api/machines/%s" % (settings['server_ip'], settings['machine_id']), settings)

    #Check if server busy
    if machine['is_busy'] and not settings['force_action']:
        write_log(settings,"info","Server busy, try again later")
        return

    for schedule in machine['schedules']:
        #Check if this schedule should procede, or wait
        if not datetime.now() > datetime.strptime(schedule['get_next_backup_time'], "%Y-%m-%d %H:%M:%S") and not settings['force_action']:
            write_log(settings,"info", "Waiting, schedule should not run before %s" % datetime.strptime(schedule['get_next_backup_time'],
                                                                                   "%Y-%m-%d %H:%M:%S"))
            continue


        if schedule['storage']['type'] != "ftp":
            write_log(settings,"error","Only FTP is supported at the moment, aborting.")
            return

        #FTP-config
        ftp_connection = ftplib.FTP(schedule['storage']['host'], schedule['storage']['username'], schedule['storage']['password'])
        ftp_folder = schedule['storage']['folder']+"/"+schedule['current_day_folder_path']

        #Set running_backup status to True
        theurl = "http://%s/api/schedules/%s/" % (settings['server_ip'], schedule['id'])
        schedule_form = {'name': schedule['name'], 'running_backup': True, 'current_version_in_loop': schedule['current_version_in_loop'],'machine_id': schedule['machine_id']}
        set_data(theurl, schedule_form, settings)

        #Performing folder backups
        for command in schedule['folder_backups']:
            write_log(settings,"info","Working on schedule %s" % command['local_folder_path'])
            save_folder_to_ftp(ftp_connection, ftp_folder, command['local_folder_path'], settings)

        #Set running_backup status to False
        schedule_form['running_backup'] = False

        next_version_number = int(schedule['current_version_in_loop'])+1
        if next_version_number > int(schedule['versions_count']):
            next_version_number = 1

        schedule_form['current_version_in_loop'] = next_version_number

        set_data(theurl, schedule_form, settings)

        #Create Backup object
        theurl = "http://%s/api/backups/" % settings['server_ip']
        new_backup_dict = {'schedule_id': schedule['id'], 'machine_id': schedule['machine_id'],
                           'time_started': datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
        set_data(theurl, new_backup_dict, settings)


def download_content(theurl, settings):
    passman = urllib2.HTTPPasswordMgrWithDefaultRealm()
    passman.add_password(None, theurl, settings['username'], settings['password'])
    authhandler = urllib2.HTTPBasicAuthHandler(passman)
    opener = urllib2.build_opener(authhandler)
    urllib2.install_opener(opener)
    pagehandle = urllib2.urlopen(theurl)
    return simplejson.loads(pagehandle.read())


def recursive_zip(zipf, directory, folder=""):
    log_file = open("log.txt","r")
    log_file_content = log_file.read()

    log_file = open("log.txt","w")
    log_file.write(log_file_content)

    for item in os.listdir(directory):
        try:
            if os.path.isfile(os.path.join(directory, item)):
                zipf.write(os.path.join(directory, item), folder + os.sep + item)
            elif os.path.isdir(os.path.join(directory, item)):
                recursive_zip(zipf, os.path.join(directory, item), folder + os.sep + item)
        except Exception, e:
            log_file.write(str(datetime.now()) + " " + str(e) + "\n")
    log_file.close()

def is_folder(path_to_folder):
    if not os.path.isdir(path_to_folder):
        return False
    if os.path.splitext(path_to_folder)[1]:
        return False
    return True


def save_at_is_zip_file(path):
    if is_folder(path):
        return False

    if os.path.splitext(path)[1] == ".zip":
        return True

    return False


def zip_folder_and_save(folder_to_zip, save_at, settings):
    if not is_folder(folder_to_zip):
        write_log(settings,"error", "Source folder is not a valid folder, you used: %s" % folder_to_zip)
        return

    if is_folder(save_at):
        write_log(settings,"error", "You have to specify a file as destination, you used: %s" % save_at)
        return

    if not save_at_is_zip_file(save_at):
        write_log(settings,"error", "ERROR: You have to specify a zip-file as destination, you used: %s" % save_at)
        return

    if os.path.exists(str(save_at)):
        os.remove(str(save_at))

    starttime = time.time()
    zipf = zipfile.ZipFile(str(save_at), mode="w")
    write_log(settings,"info","Started zipping folder %s" % str(folder_to_zip))
    recursive_zip(zipf, folder_to_zip)
    zipf.close()
    write_log(settings,"info","Done zipping folder %s, saved as %s, used %s seconds" % (
        str(folder_to_zip), str(save_at), time.time() - starttime))

def directory_exists_on_ftp_server(ftp, folder):
    filelist = []
    ftp.retrlines('LIST',filelist.append)

    for f in filelist:
        if f.split()[-1] == folder:
            return True
    return False

def create_folders_on_ftp_for_upload(ftp, ftp_folder):

    for folder in ftp_folder.split("/"):
        if folder == "":
            continue

        if directory_exists_on_ftp_server(ftp, folder):
            ftp.cwd(folder)
        else:
            ftp.mkd(folder)
            ftp.cwd(folder)

def do_upload(ftp, ftp_folder, file, file_name):

    create_folders_on_ftp_for_upload(ftp, ftp_folder)

    f = open(file, "rb")

    ftp.cwd("~/")
    ftp.storbinary("STOR %s%s" % (ftp_folder, file_name), f, 1024)
    f.close()


def do_download(ftp, ftp_folder, file, file_name):
    f = open(file, "wb")
    ftp.retrbinary("RETR /%s/%s" % (ftp_folder, file_name), f.write)
    f.close()

def create_file_name(path_to_file):
    ext = os.path.splitext(path_to_file)[1]

    separator = "/"
    if os.name == "posix":
        separator = "/"
    else:
        separator = '\\'

    file_name = ""
    for f in os.path.splitext(path_to_file)[0].split(separator):
        if f:
            file_name += f.lower() + "_"

    file_name += ext

    return file_name[:-1] + ".zip"


def save_folder_to_ftp(ftp, ftp_folder, folder_to_zip, settings):
    if not is_folder("temps"):
        os.makedirs("temps")

    file_name = create_file_name(folder_to_zip)

    local_file = "temps%s" % file_name

    zip_folder_and_save(folder_to_zip, local_file, settings)

    write_log(settings,"info", "Started uploading folder %s" % str(folder_to_zip))
    start_time = time.time()
    do_upload(ftp, ftp_folder, local_file, file_name)
    write_log(settings,"info", "Done uploading folder %s, used %s seconds" % (str(folder_to_zip), time.time() - start_time))


def extractAll(zipName, folder_to_zip):
    z = zipfile.ZipFile(zipName)
    folder_path = folder_to_zip
    for f in z.namelist():
        if f.endswith('/'):
            os.makedirs(folder_path + f)
        else:
            z.extract(f, folder_path)


def restore_backup_from_ftp(backup_id, settings):
    backup = download_content("http://%s/api/backups/%s" % (settings['server_ip'], backup_id), settings)

    if backup['schedule']['running_restore'] and not settings['force_action']:
        write_log(settings,"warning","Busy, already running restore")
        return

    if backup['schedule']['running_backup'] and not settings['force_action']:
        write_log(settings,"warning","Busy, backup in progress")
        return

    schedule_form = {'running_restore': True}
    schedule_url = "http://%s/api/schedules/%s" % (settings['server_ip'], str(backup['schedule']['id'])) + "/"
    set_data(schedule_url, schedule_form, settings)

    ftp = ftplib.FTP(backup['schedule']['ftp_host'], backup['schedule']['ftp_username'],
                     backup['schedule']['ftp_password'])
    ftp_folder = backup['schedule']['ftp_folder']

    if not is_folder("temps/restore_from_backup/"):
        os.makedirs("temps/restore_from_backup/")

    for folder in backup['schedule']['folder_backups']:
        folder_to_zip = folder['local_folder_path']
        file_name = create_file_name(folder_to_zip)

        local_file = "temps/restore_from_backup/%s" % file_name

        write_log(settings,"info","Started downloading folder %s" % str(folder_to_zip))
        start_time = time.time()
        do_download(ftp, ftp_folder, local_file, file_name)
        write_log(settings,"info","Done downloading folder %s, used %s seconds" % (str(folder_to_zip), time.time() - start_time))

        temp_file_to_zip = "temps/restore_from_backup/%s/" % str(backup_id) + folder_to_zip[1:]
        extractAll(local_file, temp_file_to_zip)

        if is_folder(folder_to_zip):
            shutil.rmtree(folder_to_zip)

        shutil.copytree(temp_file_to_zip, folder_to_zip)

        #Clean up.
    if is_folder("temps/restore_from_backup/"):
        shutil.rmtree("temps/restore_from_backup/")

    schedule_form = {'running_restore': False}
    set_data(schedule_url, schedule_form, settings)


def set_data(destination_path, data_dict, settings):
    register_openers()
    datagen, headers = multipart_encode(data_dict)
    request = urllib2.Request(destination_path, datagen, headers)
    base64string = base64.encodestring('%s:%s' % (settings['username'], settings['password'])).replace('\n', '')
    request.add_header("Authorization", "Basic %s" % base64string)
    a = urllib2.urlopen(request).read()
    return a
