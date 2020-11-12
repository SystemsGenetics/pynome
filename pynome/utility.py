"""
Detailed description.
"""
import datetime
import os
import ftplib
import subprocess
import traceback




def rSync(
    url
    ,path
    ,compare=""
    ):
    """
    Synchronizes the given remote URL file with the given local path. An
    optional comparison path is provided, which is used to compare the timestamp
    with the remote URL if given instead of the regular path.

    Parameters
    ----------
    url : string
          The remote FTP URL of a file that is synchronized with the given local
          path.
    path : string
           The full path to the local file that is synchronized with the given
           remote URL.
    compare : string
              The full path to the local file used to compare the timestamp with
              the remote in reference to synchronization. The regular path is
              still used when downloading the remote file if it is newer that
              this compared local file. If this string is empty then it is
              ignored.
    """
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
    Getter function.

    Parameters
    ----------
    url : string
          The FTP URL of a remote file whose FTP timestamp is returned.

    Returns
    -------
    ret0 : string
           The FTP timestamp of the remote file location at the given URL.
    """
    d = url.find("://")
    if d != -1:
        url = url[d+3:]
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








DAY = 86400
