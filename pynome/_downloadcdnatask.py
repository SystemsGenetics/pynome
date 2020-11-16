"""
Contains the DownloadCDNATask class.
"""
from . import interfaces
import os
import subprocess
from . import utility








class DownloadCDNATask(interfaces.AbstractTask):
    """
    This is the download CDNA task. It implements the abstract task interface.
    This synchronizes the remote CDNA Fasta file with the local assembly.
    """


    def __call__(
        self
        ):
        """
        Implements the pynome.interfaces.AbstractTask interface.

        Returns
        -------
        ret0 : object
               See interface docs.
        """
        self._log_("Syncing CDNA")
        fullPath = os.path.join(self._workDir_(),self._rootName_()+".cdna.fa")
        if utility.rSync(self._meta_()["cdna"],fullPath+".gz",compare=fullPath):
            self._log_("Decompressing CDNA")
            cmd = ["gunzip",fullPath+".gz"]
            assert(subprocess.run(cmd).returncode==0)
            return True
        else:
            return False


    def name(
        self
        ):
        """
        Implements the pynome.interfaces.AbstractTask interface.

        Returns
        -------
        ret0 : object
               See interface docs.
        """
        return "download_cdna"
