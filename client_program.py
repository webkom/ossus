import ftplib
import os
import zipfile
import time

def recursive_zip(zipf, directory, folder = ""):
   for item in os.listdir(directory):
      if os.path.isfile(os.path.join(directory, item)):
         zipf.write(os.path.join(directory, item), folder + os.sep + item)
      elif os.path.isdir(os.path.join(directory, item)):
         recursive_zip(zipf, os.path.join(directory, item), folder + os.sep + item)

def is_folder(path):
    if not os.path.isdir(path):
        return False
    if os.path.splitext(path)[1]:
        return False
    return True

def save_at_is_zip_file(path):
    if is_folder(path):
        return False

    if os.path.splitext(path)[1] == ".zip":
        return True

    return False

def zip_folder_and_save(folder_to_zip, save_at):

    if not is_folder(folder_to_zip):
        print "ERROR: Source folder is not a valid folder, you used: %s" % folder_to_zip
        return

    if is_folder(save_at):
        print "ERROR: You have to specify a file as destination, you used: %s" % save_at
        return

    if not save_at_is_zip_file(save_at):
        print "ERROR: You have to specify a zip-file as destination, you used: %s" % save_at
        return

    if os.path.exists(str(save_at)):
        os.remove(str(save_at))

    starttime = time.time()
    zipf = zipfile.ZipFile(str(save_at), mode="w" )
    print "Started zipping folder %s" % str(folder_to_zip)
    recursive_zip(zipf, folder_to_zip)
    zipf.close()
    print "Done zipping folder %s, saved as %s, used %s seconds" % (str(folder_to_zip), str(save_at), time.time()-starttime)

def do_upload(ftp, file, file_name):
    f = open(file, "rb")
    ftp.storbinary("STOR /backup/%s" % file_name, f, 1024)
    f.close()

def create_file_name(path_to_file):
    ext = os.path.splitext(path_to_file)[1]

    file_name = ""
    for f in os.path.splitext(path_to_file)[0].split("/"):
        if f:
            file_name += f.lower()+"_"

    file_name += ext

    return file_name[:-1]+".zip"

def save_folder_to_ftp(folder_to_zip):
    if not is_folder("temps"):
        os.makedirs("temps")

    file_name = create_file_name(folder_to_zip)

    local_file = "temps/%s" % file_name

    zip_folder_and_save(folder_to_zip, local_file)

    print "Started uploading folder %s" % str(folder_to_zip)

    starttime = time.time()
    s = ftplib.FTP("europa.inbusiness.no","queuefu","monset14")
    do_upload(s, local_file, file_name)
    print "Done uploading folder %s, used %s seconds" % (str(folder_to_zip), time.time()-starttime)
    s.quit()

save_folder_to_ftp("/Users/fnc/workspace/focus/")