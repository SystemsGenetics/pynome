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
    This is the index hisat task. It implements the abstract task interface.
    This indexes the local Fasta file with HiSat2.
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
        filePath = os.path.join(self._workDir_(),self._rootName_()+".fa")
        if not os.path.isfile(filePath):
            return False
        self._log_("Indexing with HiSat2")
        version = subprocess.check_output(["hisat2","--version"])
        version = version.decode().split("\n")[0].split()[-1]
        assert(re.match("^\d+\.\d+\.\d+$",version))
        for p in os.listdir(self._workDir_()):
            if p.startswith("hisat-"):
                path = os.path.join(self._workDir_(),p)
                if os.path.isdir(path):
                    cmd = ["rm","-fr",os.path.join(self._workDir_(),p)]
                    assert(subprocess.run(cmd).returncode==0)
        outDir = os.path.join(self._workDir_(),"hisat-"+version)
        os.makedirs(outDir)
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
