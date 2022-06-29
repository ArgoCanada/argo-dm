#!/usr/bin/python

from pathlib import Path
import ftplib

site = 'ftp.joubeh.com'
ftp  = ftplib.FTP(site, user='dfobio', passwd='976143')

imei_numbers = [
    '300125061656740',
    '300125061360970',
]

upload_file = Path('/Users/GordonC/Documents/argo/meds/predeployment-testing/EOL.txt')

for imei in imei_numbers:
    ftp.cwd(imei)
    file = open(upload_file,'rb')
    ftp.storbinary('STOR remote/RUDICS_cmd.txt', file)
    file.close()
    ftp.cwd('../')
ftp.quit()