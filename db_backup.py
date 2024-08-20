#!/usr/bin/env python3

import os
import time

# Variables for easy modification
date = time.strftime("%d-%m-%Y") # date format
file_path = "[/path/to/odoo.conf]" # path to your odoo.conf file
container_name = "[your_odoo_container_name]"
backup_name = "[your_backup_file_name]"
backup_format = "zip"
backup_filename = f"{date}_backup_{backup_name}.{backup_format}" # you may change the backup filename format to your liking
backup_url = "http://172.23.0.5:8069/web/database/backup" # inspect your docker network to get the correct IP
gdrive_folder_id = "[your_gdrive_folder_id]"
master_pwd = "[your_odoo_master_password]"

def clear_console():
    os.system("clear")

def allow_db_management(file_path):
    print("Allowing database management...\n")
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
        lines[11] = ';' + lines[11]
        with open(file_path, 'w') as file:
            file.writelines(lines)
        print("odoo.conf modified. Restarting container...\n")
        os.system(f"docker restart {container_name}")
        time.sleep(5)
        create_backup()
    except Exception as e:
        print(f"Error allowing database management: {str(e)}\n")
        exit()

def deny_db_management(file_path):
    print("Denying database management...\n")
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
        lines[11] = lines[11].lstrip(';')
        with open(file_path, 'w') as file:
            file.writelines(lines)
        os.system(f"docker restart {container_name}")
        print("\nodoo.conf modified. Restarting container...\n")
    except Exception as e:
        print(f"Error denying database management: {str(e)}\n")
        exit()

def create_backup():
    print("\nCreating backup...\n")
    try:
        os.system(f"curl -X POST -F 'master_pwd={master_pwd}' -F 'name={backup_name}' -F 'backup_format={backup_format}' -o ./{backup_filename} {backup_url}")
        print("\nBackup created successfully.\n")
        upload_to_cloud()
    except Exception as e:
        print(f"Error creating backup: {str(e)}\n")
        exit()

def upload_to_cloud():
    print("\nUploading backup to cloud...\n")
    try:
        os.system(f"gdrive files upload --parent {gdrive_folder_id} {backup_filename}")
        print("\nBackup uploaded to cloud successfully.\n")
        delete_backup()
    except Exception as e:
        print(f"\nError uploading backup to cloud: {str(e)}\n")
        exit()

def delete_backup():
    try:
        os.system(f"rm -rf {backup_filename}")
        print("Local backup deleted successfully.\n")
        deny_db_management(file_path)
    except Exception as e:
        print(f"Error deleting backup: {str(e)}\n")
        exit()

if __name__ == "__main__":
    clear_console()
    allow_db_management(file_path)
    
