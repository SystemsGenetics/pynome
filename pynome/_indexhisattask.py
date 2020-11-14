"""
Contains the IndexHisatTask class.
"""
from . import interfaces
import os
import re
from . import settings
import subprocess








class IndexHisatTask(interfaces.AbstractTask):
    """
    Detailed description.
    """


    def __call__(
        self
        ):
        """
        Detailed description.
        """
        filePath = os.path.join(self._workDir_(),self._rootName_()+".fa")
        if not os.path.isfile(filePath):
            return False
        self._log_("Indexing with HiSat2")
        version = subprocess.check_output(["hisat2","--version"])
        version = version.decode().split("\n")[0].split()[-1]
        assert(re.match("^\d+\.\d+\.\d+$",version))
        outDir = os.path.join(self._workDir_(),"hisat-"+version)
        os.makedirs(outDir,exist_ok=True)
        outBase = os.path.join(outDir,self._rootName_())
        cmd = ["hisat2-build","--quiet","-p",str(settings.cpuCount),"-f",filePath,outBase]
        assert(subprocess.run(cmd).returncode==0)
        return True


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
        return "index_hisat"
