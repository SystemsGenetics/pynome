"""
Contains the FTPGunzip class.
"""
import os
import datetime
import ftplib
import subprocess
import traceback
from . import abstract
from . import core








class FTPGunzip(abstract.AbstractMirror):
    """
    This is the FTP Gunzip class. It implements the abstract mirror interface.
    This mirror implementation takes the FTP location of the FASTA and GFF file,
    downloads both using wget, and then runs gunzip to deliver the final
    uncompressed data files.
    """


    #######################
    # PUBLIC - Initialize #
    #######################


    def __init__(
        self
        ):
        """
        Initializes a new FTP Gunzip mirror instance.
        """
        abstract.AbstractMirror.__init__(self)


    ####################
    # PUBLIC - Methods #
    ####################


    def mirror(
        self
        ,workingDir
        ,rootName
        ,meta
        ):
        """
        Implements the pynome2.abstract.AbstractMirror interface.

        Parameters
        ----------
        workingDir : object
                     See interface docs.
        rootName : object
                   See interface docs.
        meta : object
               See interface docs.

        Returns
        -------
        ret0 : object
               See interface docs.
        """
        (fasta,gff3) = self.__downloadDirectives_(os.path.join(workingDir,rootName),meta)
        if fasta:
            core.log.send("Downloading FTP FASTA "+rootName)
            cmd = ["wget",meta["fasta"],"-q","-O",os.path.join(workingDir,rootName+".fa.gz")]
            assert(subprocess.run(cmd).returncode==0)
            core.log.send("Decompressing FTP FASTA "+rootName)
            cmd = ["gunzip",os.path.join(workingDir,rootName+".fa.gz")]
            assert(subprocess.run(cmd).returncode==0)
        if gff3:
            core.log.send("Downloading FTP GFF3 "+rootName)
            cmd = ["wget",meta["gff3"],"-q","-O",os.path.join(workingDir,rootName+".gff3.gz")]
            assert(subprocess.run(cmd).returncode==0)
            core.log.send("Decompressing FTP GFF3 "+rootName)
            cmd = ["gunzip",os.path.join(workingDir,rootName+".gff3.gz")]
            assert(subprocess.run(cmd).returncode==0)
        return (fasta,gff3)


    #####################
    # PRIVATE - Methods #
    #####################


    def __downloadDirectives_(
        self
        ,rootPath
        ,meta
        ):
        """
        Detailed description.

        Parameters
        ----------
        rootPath : object
                   Detailed description.
        meta : object
               See interface docs.
        """
        fasta = False
        gff3 = False
        if not os.path.isfile(rootPath+".fa"):
            fasta = True
        else:
            rts = self.__timeStamp_(meta["fasta"])
            lts = datetime.datetime.fromtimestamp(
                os.stat(rootPath+".fa").st_mtime+86400
            ).strftime("%Y%m%d%H%M%S")
            if rts > lts:
                fasta = True
        if not os.path.isfile(rootPath+".gff3"):
            gff3 = True
        else:
            rts = self.__timeStamp_(meta["gff3"])
            lts = datetime.datetime.fromtimestamp(
                os.stat(rootPath+".gff3").st_mtime+86400
            ).strftime("%Y%m%d%H%M%S")
            if rts > lts:
                gff3 = True
        return (fasta,gff3)


    def __timeStamp_(
        self
        ,url
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
