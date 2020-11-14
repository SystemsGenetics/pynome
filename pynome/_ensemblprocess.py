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
    INPUTS = {
        "index_hisat": [".fa"]
        ,"write_gtf": [".gff"]
        ,"index_salmon": [".cdna.fa"]
        ,"index_kallisto": [".cdna.fa"]
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


    def taskInputs(
        self
        ,taskName
        ):
        """
        Detailed description.

        Parameters
        ----------
        taskName : object
                   Detailed description.
        """
        return self.INPUTS.get(taskName,[])


    def taskSources(
        self
        ,taskName
        ):
        """
        Detailed description.

        Parameters
        ----------
        taskName : object
                   Detailed description.
        """
        return self.DEPS.get(taskName,[])
