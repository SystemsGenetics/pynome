"""
Contains the FTPGunzip class.
"""
import os
import ftplib
import subprocess
from . import abstract
from . import core
from . import utility








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


    def mirrorFasta(
        self
        ,workingDir
        ,path
        ,meta
        ,title
        ):
        """
        Implements the pynome2.abstract.AbstractMirror interface.

        Parameters
        ----------
        workingDir : object
                     See interface docs.
        path : object
               See interface docs.
        meta : object
               See interface docs.
        title : object
                See interface docs.

        Returns
        -------
        ret0 : object
               See interface docs.
        """
        core.log.send("Syncing FASTA "+title)
        fullPath = os.path.join(workingDir,path)
        if utility.rSync(meta["fasta"],fullPath+".gz",compare=fullPath):
            core.log.send("Decompressing FASTA "+title)
            cmd = ["gunzip",fullPath+".gz"]
            assert(subprocess.run(cmd).returncode==0)
            return True
        else:
            return False


    def mirrorGff(
        self
        ,workingDir
        ,path
        ,meta
        ,title
        ):
        """
        Implements the pynome2.abstract.AbstractMirror interface.

        Parameters
        ----------
        workingDir : object
                     See interface docs.
        path : object
               See interface docs.
        meta : object
               See interface docs.
        title : object
                See interface docs.

        Returns
        -------
        ret0 : object
               See interface docs.
        """
        core.log.send("Syncing GFF "+title)
        fullPath = os.path.join(workingDir,path)
        if utility.rSync(meta["gff"],fullPath+".gz",compare=fullPath):
            core.log.send("Decompressing GFF "+title)
            cmd = ["gunzip",fullPath+".gz"]
            assert(subprocess.run(cmd).returncode==0)
            return True
        else:
            return False
