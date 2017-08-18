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


class GenomeEntry(object):
    """
    Class that holds indivudual genome entries.
    """
    # pylint: disable=too-many-instance-attributes
    # These are the attributes needed for each genome entry.
    # Slots ensure low memory usage.
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
        'sra_id',
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
                 sra_id=None):
        """Create the funciton with optional arguments..."""
        self.taxonomic_name = taxonomic_name
        self.download_method = download_method
        self.fasta_uri = fasta_uri
        self.gff3_uri = gff3_uri
        self.local_path = local_path
        self.fasta_remote_size = fasta_remote_size
        self.gff3_remote_size = gff3_remote_size
        self.assembly_name = assembly_name
        self.genus = genus
        self.species = species
        self.sra_id = sra_id

    def __repr__(self):
        return 'Genome Entry({0.taxonomic_name})'.format(self)

    def __str__(self):
        out_str = (
            '\nTaxonomic Name: {0.taxonomic_name:>30}\n'
            'Genus: {0.genus:>30}\n'
            'Species: {0.species:>30}\n'
            'Assembly Name: {0.assembly_name:>30}\n'.format(self)
        )
        return out_str


class GenomeDatabase(object):
    """Base Genome Database class. Many functions will be overwritten by
    the database-specific child classes.

    .. warning:: **This class should not be directly called.**
        It must be implemented with a child class to fill out certain
        functions."""

    def __init__(self):
        """Initialization of the GenomeDatabase class."""
        self.genome_list = {}

    def __str__(self):
        """Custom string representation method."""
        return str([genome for genome in self.genome_list])

    def save_genome(self, genome):
        """Save the genomes in this database. Save to the _baseGenomeDir
         location."""
        self._save_genome(genome)
        return

    def _save_genome(self, genome):
        """Appends a genome tuple to the list."""
        # Generate the key, which is taxonomic name merged with the assembly
        pass

    def find_genomes(self):
        """To be overwritten by child classes. Very database specific."""
        pass

    def download_genomes(self):
        """To be overwritten by child classes. Very database specific."""
        pass
