"""
Contains the IndexKallistoTask class.
"""
from . import interfaces
import os
import re
import subprocess








class IndexKallistoTask(interfaces.AbstractTask):
    """
    This is the index kallisto task. It implements the abstract task interface.
    This indexes the local CDNA Fasta file with Kallisto.
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
        filePath = os.path.join(self._workDir_(),self._rootName_()+".cdna.fa")
        if not os.path.isfile(filePath):
            return False
        self._log_("Indexing with Kallisto")
        version = subprocess.check_output(["kallisto","version"])
        version = version.decode().split("\n")[0].split()[-1]
        assert(re.match("^\d+\.\d+\.\d+$",version))
        outBase = os.path.join(self._workDir_(),"kallisto-"+version)
        os.makedirs(outBase,exist_ok=True)
        outBase = os.path.join(outBase,self._rootName_()+".idx")
        cmd = [
            "kallisto"
            ,"index"
            ,"--index"
            ,outBase
            ,filePath
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
        return "index_kallisto"
