"""
Contains the NCBIProcess class.
"""
from . import interfaces








class NCBIProcess(interfaces.AbstractProcess):
    """
    Detailed description.
    """
    DEPS = {
        "index_hisat": ["download_fasta"]
        ,"write_gtf": ["download_gff"]
        ,"write_splice_sites": ["write_gtf","download_gtf"]
        ,"write_cdna": ["write_gtf","download_gtf"]
        ,"index_salmon": ["write_cdna"]
        ,"index_kallisto": ["write_cdna"]
    }
    INPUTS = {
        "index_hisat": [".fa"]
        ,"write_gtf": [".gff"]
        ,"write_splice_sites": [".gtf"]
        ,"write_cdna": [".fa",".gtf"]
        ,"index_salmon": [".cdna.fa"]
        ,"index_kallisto": [".cdna.fa"]
    }


    def indexTasks(
        self
        ):
        """
        Detailed description.
        """
        return ("index_hisat","write_gtf","write_splice_sites","write_cdna","index_salmon","index_kallisto")


    def mirrorTasks(
        self
        ):
        """
        Detailed description.
        """
        return ("download_fasta","download_gff","download_gtf")


    def name(
        self
        ):
        """
        Detailed description.
        """
        return "ncbi"


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
