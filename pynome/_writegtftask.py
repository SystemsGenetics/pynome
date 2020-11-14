"""
Contains the WriteGtfTask class.
"""
from . import interfaces
import os
import subprocess








class WriteGtfTask(interfaces.AbstractTask):
    """
    Detailed description.
    """


    def __call__(
        self
        ):
        """
        Detailed description.
        """
        basePath = os.path.join(self._workDir_(),self._rootName_())
        if not os.path.isfile(basePath+".gff"):
            return False
        self._log_("Writing GTF from GFF")
        tPath = os.path.join(self._workDir_(),"temp.gff")
        cmd = ["cp",basePath+".gff",tPath]
        assert(subprocess.run(cmd).returncode==0)
        cmd = ["gffread","-T",tPath,"-o",basePath+".gtf"]
        assert(subprocess.run(cmd).returncode==0)
        cmd = ["rm",tPath]
        assert(subprocess.run(cmd).returncode==0)
        with open(basePath+".Splice_sites",'w') as ofile:
            self._log_("Writing Spice sites from GTF")
            cmd = ['hisat2_extract_splice_sites.py',basePath+".gtf"]
            assert(subprocess.run(cmd,stdout=ofile).returncode==0)
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
        return "write_gtf"
