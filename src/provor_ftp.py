#!/usr/bin/python

import sys
from pathlib import Path
import ftplib

site = 'ftp.joubeh.com'
ftp  = ftplib.FTP(site, user='dfobio', passwd=sys.stdin[1])

for imei in ftp.nlst():
    ftp.cwd(imei)
    for fn in ftp.nlst('*.bin'):
        local_file = Path('../data/provor') / imei / fn
        if not local_file.parent.exists():
            local_file.parent.mkdir()
        if not local_file.exists():
            sys.stdout.write(f'Downloading {imei}/{fn}...')
            lf = open(local_file, 'wb')
            ftp.retrbinary('RETR ' + fn, lf.write)
            lf.close()
            sys.stdout.write('done\n')
    ftp.cwd('../')

for imei in ftp.nlst():
    ftp.cwd(imei)
    for fn in ftp.nlst('*.txt'):
        local_file = Path('../data/provor') / imei / fn
        if not local_file.parent.exists():
            local_file.parent.mkdir()
        if not local_file.exists():
            sys.stdout.write(f'Downloading {imei}/{fn}...')
            lf = open(local_file, 'wb')
            ftp.retrbinary('RETR ' + fn, lf.write)
            lf.close()
            sys.stdout.write('done\n')
    ftp.cwd('../')

for imei in ftp.nlst():
    ftp.cwd(imei)
    for fn in ftp.nlst('*.hex'):
        local_file = Path('../data/provor') / imei / fn
        if not local_file.parent.exists():
            local_file.parent.mkdir()
        if not local_file.exists():
            sys.stdout.write(f'Downloading {imei}/{fn}...')
            lf = open(local_file, 'wb')
            ftp.retrbinary('RETR ' + fn, lf.write)
            lf.close()
            sys.stdout.write('done\n')
    ftp.cwd('../')