"""
Contains the IndexSalmonTask class.
"""
from . import interfaces
import os
import re
from . import settings
import subprocess








class IndexSalmonTask(interfaces.AbstractTask):
    """
    Detailed description.
    """


    def __call__(
        self
        ):
        """
        Detailed description.
        """
        filePath = os.path.join(self._workDir_(),self._rootName_()+".cdna.fa")
        if not os.path.isfile(filePath):
            return False
        self._log_("Indexing with Salmon")
        version = subprocess.check_output(["salmon","--version"])
        version = version.decode().split("\n")[0].split()[-1]
        assert(re.match("^\d+\.\d+\.\d+$",version))
        cmd = [
            "salmon"
            ,"index"
            ,"--index"
            ,os.path.join(self._workDir_(),"salmon-"+version)
            ,"--transcripts"
            ,filePath
            ,"--threads"
            ,str(settings.cpuCount)
        ]
        assert(subprocess.run(cmd,capture_output=True).returncode==0)
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
        return "index_salmon"
