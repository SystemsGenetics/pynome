# I am not sure if this should go here.
import logging

logging.basicConfig(filename='pynome.genome.log', level=logging.DEBUG)
logging.debug("Pynome.Genome module initialized.")


# TODO: Parameter strings are not correct?
# TODO: Docstrings are not in PEP8 format.

class Genome:
    """
    @brief    Instance of a Genome class.

    @param    _gff3       String. Local directory of the gff3 file.
    @param    _fasta      String. Local directory of the fasta file.
    @param    _assembly_version    String. TODO: Add description.
    @param    taxonomic_name      String. TODO: Add example.
    """

    def __index__(self):
        """
        @brief     Initialization of the Genome class.
                   Creates t
        """
        self._gff3 = None  # local directory of gff3 file
        self._fasta = None  # local directory of fasta file
        self._assembly_version = None
        self._taxonomic_name = None

        logging.debug("Genome initialized.")

    @property
    def assembly_version(self):
        """
        @brief     Assembly version property.
                   Should be a string value in the form of:
                        "TODO: examplolus specius"
        """
        return self._assembly_version

    @property
    def taxonomic_name(self):
        """
        @brief     Taxonomic Name property.

        @return    A string is returned in the form of TODO: format.
        """
        return self._taxonomic_name

    @property
    def gff3(self):
        """
        @brief     .gff3 local filepath property.
        """
        return self._gff3

    @property
    def fasta(self):
        """
        @brief     .fasta local file path property
        """
        return self._fasta

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
