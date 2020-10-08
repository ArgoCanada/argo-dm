#!/usr/bin/python

from pathlib import Path
import ftplib

url = 'ftp.ifremer.fr'
loc = '/ifremer/argo/etc/trajectoryBcCombined_SampleFiles/v3_2/'

ftp = ftplib.FTP(url)
ftp.login()
ftp.cwd(loc)

local_path = Path('/Users/gordonc/Documents/data/Argo-DM')
if not local_path.exists():
    local_path.mkdir()

for fn in ftp.nlst():
    print(fn)
    local_file = local_path / fn
    lf = open(local_file, 'wb')
    # retrieve the file on FTP server,
    ftp.retrbinary('RETR ' + fn, lf.write)
    lf.close()