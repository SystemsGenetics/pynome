"""
Contains the DownloadGtfTask class.
"""
from . import interfaces
import os
import subprocess
from . import utility








class DownloadGtfTask(interfaces.AbstractTask):
    """
    This is the download Gtf task. It implements the abstract task interface.
    This synchronizes the remote Gtf file with the local assembly. If the Gtf
    URL entry in the metadata is empty then this does nothing.
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
        if not self._meta_().get("gtf",""):
            return False
        self._log_("Syncing GTF")
        fullPath = os.path.join(self._workDir_(),self._rootName_()+".gtf")
        if utility.rSync(self._meta_()["gtf"],fullPath+".gz",compare=fullPath):
            self._log_("Decompressing GTF")
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
        return "download_gtf"
