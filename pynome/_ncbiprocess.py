"""
Contains the NCBIProcess class.
"""
from . import interfaces








class NCBIProcess(interfaces.AbstractProcess):
    """
    This is the NCBI process class. It implements the abstract process
    interface. This provides all tasks required for assemblies crawled from
    NCBI.
    """
    DEPS = {
        "index_hisat": ["download_fasta"]
        ,"write_gtf": ["download_gff"]
        ,"write_splice_sites": ["write_gtf","download_gtf"]
        ,"write_cdna": ["write_gtf","download_gtf","download_fasta"]
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
        Implements the pynome.interfaces.AbstractProcess interface.

        Returns
        -------
        ret0 : object
               See interface docs.
        """
        return (
            "index_hisat"
            ,"write_gtf"
            ,"write_splice_sites"
            ,"write_cdna"
            ,"index_salmon"
            ,"index_kallisto"
        )


    def mirrorTasks(
        self
        ):
        """
        Implements the pynome.interfaces.AbstractProcess interface.

        Returns
        -------
        ret0 : object
               See interface docs.
        """
        return ("download_fasta","download_gff","download_gtf")


    def name(
        self
        ):
        """
        Implements the pynome.interfaces.AbstractProcess interface.

        Returns
        -------
        ret0 : object
               See interface docs.
        """
        return "ncbi"


    def taskInputs(
        self
        ,taskName
        ):
        """
        Implements the pynome.interfaces.AbstractProcess interface.

        Parameters
        ----------
        taskName : object
                   See interface docs.

        Returns
        -------
        ret0 : object
               See interface docs.
        """
        return self.INPUTS.get(taskName,[])


    def taskSources(
        self
        ,taskName
        ):
        """
        Implements the pynome.interfaces.AbstractProcess interface.

        Parameters
        ----------
        taskName : object
                   See interface docs.

        Returns
        -------
        ret0 : object
               See interface docs.
        """
        return self.DEPS.get(taskName,[])
