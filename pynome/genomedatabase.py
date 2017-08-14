"""
==========================
The Genome Database Module
==========================

The **Genomedatabase** module consists of two classes:

    + :class:`GenomeEntry` - An ``sql declarative_base()`` instance.
    + :py:class:`GenomeDatabase` - The handler for above, and the parent\
        class for specific databases to be overloaded.
"""

import collections

try:
    from tqdm import tqdm
except ImportError:
    def tqdm(*args, **kwargs):
        if args:
            return args[0]
        return kwargs.get('iterable', None)


class GenomeTuple(collections.namedtuple(
    'Genome',  # The typename
    # The field_names
    ['taxonomic_name', 'download_method', 'fasta_uri', 'gff3_uri',
     'local_path', 'fasta_remote_size', 'gff3_remote_size',
     'assembly_name', 'genus', 'sra_ID'])):
    """The namedtuble subclass that will act as the holder for
    desired genomic data."""

    def __repr__(self):
        """The function that determines the format and content of
        terminal print calls."""
        field_name_repr = [
            '{0:25} : {1}\n'.format(name, getattr(self, name))
            for name in self._fields
        ]

        out_str = '\n===={}====\n'.format(
            self.taxonomic_name) + ''.join(field_name_repr)
        return out_str


class GenomeDatabase(object):
    """Base Genome Database class. Many functions will be overwritten by
    the database-specific child classes.

    .. warning:: **This class should not be directly called.**
        It must be implemented with a child class to fill out certain
        functions."""

    def __init__(self):
        """Initialization of the GenomeDatabase class."""
        # Create attributes that are not related to SQLAlchemy.
        pass

    def save_genome(self, taxonomic_name, **kwargs):
        """Save the genomes in this database. Save to the _baseGenomeDir
         location."""
        self._save_genome(taxonomic_name, **kwargs)
        return

    def _save_genome(self, taxonomic_name, **kwargs):
        """TODO:"""
        pass

    def print_genomes(self):
        """Print all the Genomes in the database to the terminal."""
        pass

    def find_genomes(self):
        """To be overwritten by child classes. Very database specific."""
        pass

    def download_genomes(self):
        """To be overwritten by child classes. Very database specific."""
        pass
