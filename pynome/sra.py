"""
===================
SRA Retrival Module
===================

SRA values to be obtained here:

https://www.ncbi.nlm.nih.gov/sra

Here's the summary of our filter criteria:

    1)  read length >-= 100bp
    2)  # of spots (reads):  15 Million
    3)  PAIRED reads only
    4)  Species with genome and GFF3 file.
    5)  Illumina sequencers.

"""

from pynome import genomedatabase


class SRADatabase(genomedatabase.GenomeDatabase):
    """
    ------------
    SRA Database
    ------------
    """
    def find_genomes():
    	"""
		Find the SRA identifiers.

		::

    	"""