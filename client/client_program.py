# -*- coding: utf-8 -*-
import ftplib
import os
from backup_system import restore_backup_from_ftp
from backup_system import run_check

settings = {
    'server_ip': "localhost:8000",
    'machine_id': "12312423",
    'username': '',
    'password': '',
    'os': '',
    'force_action': True,
}

run_check(settings)
#ftp_connection = ftplib.FTP("europa.inbusiness.no", "queuefu", "monset14")

"""
def delete_fto_folder(folder):
    for file in ftp_connection.nlst(folder):
        if file == '.' or file == '..':
            continue
        if os.path.splitext(str(file))[1]:
            ftp_connection.delete("%s/%s" % (folder,file))
        else:
            delete_fto_folder(folder+"/"+file)

    ftp_connection.rmd(folder)
        
delete_fto_folder("backup")
"""