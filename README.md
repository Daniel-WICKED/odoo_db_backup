# odoo_db_backup
Python script to automate backups for odoo databases and upload them to google drive with one command

This script is intended to use it directly on the server where the Odoo instance is deployed (tested with containerized odoo instances using docker)

Make sure to setup the necessary permissions for the script to be run easily with one command, for example ./db_backup.py

This script works with gdrive to upload files to google drive, you may want to explore ways to use a different cloud storage if you need. GDrive setup: https://github.com/glotlabs/gdrive

