"""
Contains the DownloadFastaTask class.
"""
from . import interfaces
import os
import subprocess
from . import utility








class DownloadFastaTask(interfaces.AbstractTask):
    """
    Detailed description.
    """


    def __call__(
        self
        ):
        """
        Detailed description.
        """
        self._log_("Syncing FASTA")
        fullPath = os.path.join(self._workDir_(),self._rootName_()+".fa")
        if utility.rSync(self._meta_()["fasta"],fullPath+".gz",compare=fullPath):
            self._log_("Decompressing FASTA")
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
        return "download_fasta"
