"""
Contains the DownloadGffTask class.
"""
from . import interfaces
import os
import subprocess
from . import utility








class DownloadGffTask(interfaces.AbstractTask):
    """
    Detailed description.
    """


    def __call__(
        self
        ):
        """
        Detailed description.
        """
        if not self._meta_().get("gff",""):
            return False
        self._log_("Syncing GFF")
        fullPath = os.path.join(self._workDir_(),self._rootName_()+".gff")
        if utility.rSync(self._meta_()["gff"],fullPath+".gz",compare=fullPath):
            self._log_("Decompressing GFF")
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
        return "download_gff"
