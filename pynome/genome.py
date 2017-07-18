# I am not sure if this should go here.
import logging
import logging.config

# TODO: Docstrings are not in PEP8 format.


class Genome(object):  # (object) should not be needed with python3.6
    """
    The Genome class
    """

    def __init__(self):
        """
        @brief     Initialization of the Genome class.
        """
        self._gff3 = None  # local directory of gff3 file
        self._fasta = None  # local directory of fasta file
        self._assembly_version = None
        self._taxonomic_name = None
        
        logging.config.fileConfig('pynome/pynomeLog.conf')
        self.logger = logging.getLogger('pynomeLog')


    @property
    def assembly_version(self):
        """Assembly version property."""
        return self._assembly_version

    @assembly_version.setter
    def assembly_version(self, value):
        """Setter for the assembly version property."""
        # TODO: Add code to ensure value is a valid assembly number.
        self._assembly_version = value

    @assembly_version.deleter
    def assembly_version(self):
        del self._assembly_version

    @property
    def taxonomic_name(self):
        """Taxonomic Name property. """
        return self._taxonomic_name

    @taxonomic_name.setter
    def taxonomic_name(self, value):
        """Taxonomic name setter."""
        # TODO: Add validation for taxonomic name setter.
        self._taxonomic_name = value

    @taxonomic_name.deleter
    def taxonomic_name(self):
        del self._taxonomic_name

    @property
    def gff3(self):
        """.gff3 local filepath property."""
        return self._gff3

    @gff3.setter
    def gff3(self, value):
        """gff3 file path setter."""
        self._gff3 = value

    @gff3.deleter
    def gff3(self):
        del self._gff3

    @property
    def fasta(self):
        """fasta local file path property"""
        return self._fasta

    @fasta.setter
    def fasta(self, value):
        """local fasta path setter"""
        self._fasta = value

    @fasta.deleter
    def fasta(self):
        del self._fasta

    def _decompress_file(self):
        """
        @brief     Decompress a gff3.ga or fa.gz file.
        """
        pass

    def _compress_file(self):
        """
        @brief     Compress a TODO: to a gff3.ga or fa.gz file.
        """
        pass

    def get_file_prefix(self):
        """
        @brief     Builds a string prefix for all genome associated files.

        @return    Returns a string prefix for this genomes associated files.
        """
        pass

    def print_genome(self):
        """
        @brief     Prints this genome to the terminal.
                   TODO: determine the format for output.
        """
        pass

    def build_gtf(self):
        """
        @brief     Builds the gtf file from the corresponding gff3 file.

        @returns   TODO: What should this return?
        """
        pass

    def build_index(self):
        """
        @brief     Uses the hisat2 tool to build the index from the .fa file.

        @return    TODO: Implement function. Also determine what this should return.
                   If anything.
        """
        pass

    def build_splice_sites(self):
        """
        @brief      uses the hisat2_extract_splice_sites.py
                    TODO: Implement & learn the hisat2 tool.
                    TODO: look at the python script mentioned above.
        """
        pass
