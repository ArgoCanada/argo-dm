#!/usr/bin/python

from pathlib import Path
import ftplib

site = 'ftp.joubeh.com'
ftp  = ftplib.FTP(site, user='dfobio', passwd='976143')

for imei in ftp.nlst():
    ftp.cwd(imei)
    for fn in ftp.nlst()[:-1]:
        local_file = Path('../data/provor') / imei / fn
        if not local_file.parent.exists():
            local_file.parent.mkdir()
        lf = open(local_file, 'wb')
        ftp.retrbinary('RETR ' + fn, lf.write)
        lf.close()
    ftp.cwd('../')