"""
==========================
The Genome Database Module
==========================

The **Genomedatabase** module consists of two classes:

    + :class:`GenomeEntry`
    + :py:class:`GenomeDatabase` - The handler for above, and the parent\
        class for specific databases to be overloaded.
"""

import collections
import json
import logging
# from tqdm import tqdm


# GenomeDict = dict({
#     'taxonomic_name': None,
#     'download_method': None,
#     'fasta_uri': None,
#     'gff3_uri': None,
#     'local_path': None,
#     'fasta_remote_size': None,
#     'gff3_remote_size': None,
#     'assembly_name': None,
#     'genus': None,
#     'species': None,
#     'sra_ID': None
# })


class GenomeEntry(object):
    __slots__ = [
        'taxonomic_name',
        'download_method',
        'fasta_uri',
        'gff3_uri',
        'local_path',
        'fasta_remote_size',
        'gff3_remote_size',
        'assembly_name',
        'genus',
        'species',
        'sra_ID',
    ]

    def __init__(self,
                 taxonomic_name=None,
                 download_method=None,
                 fasta_uri=None,
                 gff3_uri=None,
                 local_path=None,
                 fasta_remote_size=None,
                 gff3_remote_size=None,
                 assembly_name=None,
                 genus=None,
                 species=None,
                 sra_ID=None):
        """Create the funciton with optional arguments..."""

    def __repr__(self):
        out_str = '{}'.format(self.taxonomic_name)
        return out_str


class GenomeDatabase(object):
    """Base Genome Database class. Many functions will be overwritten by
    the database-specific child classes.

    .. warning:: **This class should not be directly called.**
        It must be implemented with a child class to fill out certain
        functions."""

    def __init__(self):
        """Initialization of the GenomeDatabase class."""
        self.genome_list = []

    def __repr__(self):
        # [str(item) for item in mylist]
        return str(self.genome_list)

    def save_genome(self, genome):
        """Save the genomes in this database. Save to the _baseGenomeDir
         location."""
        self._save_genome(genome)
        return

    def _save_genome(self, genome):
        """Appends a genome tuple to the list."""
        if genome in self.genome_list:
            genome._replace(**genome.asdict())
            # update the list with the arguments from genome.
        self.genome_list.append(genome)

    def find_genomes(self):
        """To be overwritten by child classes. Very database specific."""
        pass

    def download_genomes(self):
        """To be overwritten by child classes. Very database specific."""
        pass
