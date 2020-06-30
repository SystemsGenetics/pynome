"""
Detailed description.
"""
import datetime
import os
import ftplib
import subprocess
import traceback


#
# int The amount of seconds in one day or 24 hours.
#
DAY = 86400




def rSync(
    url
    ,path
    ,compare=""
    ):
    """
    Detailed description.

    Parameters
    ----------
    url : object
          Detailed description.
    path : object
           Detailed description.
    compare : object
              Detailed description.
    """
    d = url.find("://")
    if d != -1:
        url = url[d+3:]
    if not compare:
        compare = path
    download = False
    if not os.path.isfile(compare):
        download = True
    else:
        rts = timeStamp(url)
        lts = datetime.datetime.fromtimestamp(os.stat(compare).st_mtime+DAY)
        lts = lts.strftime("%Y%m%d%H%M%S")
        if rts > lts:
            download = True
    if download:
        cmd = [
            "wget"
            ,url
            ,"-O"
            ,path
        ]
        assert(subprocess.run(cmd,capture_output=True).returncode==0)
        return True
    else:
        return False




def timeStamp(
    url
    ):
    """
    Detailed description.

    Parameters
    ----------
    url : object
          Detailed description.
    """
    site = url[:url.find("/")]
    path = url[url.find("/"):]
    try:
        ftp = ftplib.FTP(site)
        ftp.login()
        ts = ftp.voidcmd("MDTM "+path)
        return ts.split()[-1].strip()
    except:
        traceback.print_exc()
        return "0"
