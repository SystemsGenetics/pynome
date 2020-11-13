"""
Contains the EnsemblProcess class.
"""
from . import interfaces








class EnsemblProcess(interfaces.AbstractProcess):
    """
    Detailed description.
    """
    DEPS = {
        "index_hisat": ["download_fasta"]
        ,"write_gtf": ["download_gff"]
        ,"index_salmon": ["download_cdna"]
        ,"index_kallisto": ["download_cdna"]
    }


    def indexTasks(
        self
        ):
        """
        Detailed description.
        """
        return ("index_hisat","write_gtf","index_salmon","index_kallisto")


    def mirrorTasks(
        self
        ):
        """
        Detailed description.
        """
        return ("download_fasta","download_gff","download_cdna")


    def name(
        self
        ):
        """
        Detailed description.
        """
        return "ensembl"


    def taskSources(
        self
        ,task
        ):
        """
        Detailed description.

        Parameters
        ----------
        task : object
               Detailed description.
        """
        return self.DEPS.get(task,[])
