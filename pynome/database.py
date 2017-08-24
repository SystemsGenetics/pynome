
"""
==========================
The Genome Database Module
==========================
The **Genomedatabase** module consists of two classes:
"""

import logging
from pynome import Session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, create_engine


Base = declarative_base()


class GenomeEntry(Base):  # Inherit from declarative_base.
    """A sqlite handler for the GenomeTable database.

    This supposedly will both create the desired sql table, as well as
    act as the handler for generating new row entries into said table.
    To add a record to the database, an instance of this class must be
    initialized with the desired data within. Then that new instance of
    the GenomeEntry will be added to the session, and then committed.
    Each GenomeEntry has:

    :param taxonomic_name: The taxonomic name and primary key of
                           the GenomeEntry.
    :param download_method: The Download method. Stored as
                            ``<method_name> <database>``
    :param fasta_uri: The fa.gz url as a String. Max Chars = 1000.
    :param gff3_uri: The gff3.gz uri as a String. Max Chars = 1000.
    :param genome_local_path: The local path of this genome as a String.
                              Max Chars = 1000.
    :param gff3_size: The remote size of the gff3.gz file as an Integer.
    :param fasta_size: The remote size of the fa.gz file as an Integer.
    :param assembly_name: The name of the assembly.
    :param genus: The genus of the assembly.

    :Examples:

    An instance of this class should be created whenever a genome entry
    needs to be created or modified.

        >>> newGenome = GenomeEntry([taxonomic_name], **kwargs)

    In deployments this will be handled by a wrapper function specific
    to the database being examined.
    """
    __tablename__ = "GenomeTable"  # Should this be the same as the class?
    taxonomic_name = Column(String(150), primary_key=True)
    download_method = Column(String(10))
    local_path = Column(String(300))
    species = Column(String(150))
    fasta_uri = Column(String(1000))
    gff3_uri = Column(String(1000))
    genome_local_path = Column(String(1000))
    gff3_size = Column(Integer())
    fasta_size = Column(Integer())
    assembly_name = Column(String(250))
    genus = Column(String(250))
    taxonomy_id = Column(String(100))

    def __init__(self, taxonomic_name, **kwargs):
        """Constructor that overrides the default provided. This ensures that
        a taxonomic_name is required for each GenomeEntry."""
        self.taxonomic_name = taxonomic_name
        for key, value in kwargs.items():  # Set attributes found in **kwargs
            setattr(self, key, value)

    def __str__(self):
        """Custom representation that will be pulled up when a print out
        is requested."""
        out_str = (
            "\n"
            "Taxonomic Name: {0.taxonomic_name}\n"
            "\tfasta URI: {0.fasta_uri}\n"
            "\tgff3 URI: {0.gff3_uri}\n"
            .format(self)
        )
        return out_str


class GenomeDatabase(object):
    """Base Genome Database class. Many functions will be overwritten by
    the database-specific child classes.
    :param path: the sql database path.

    .. warning:: **This class should not be directly called.**
        It must be implemented with a child class to be useful."""

    def __init__(self, download_path, database_path):
        """Initialization of the GenomeDatabase class."""
        self.download_path = download_path  # The local download location.
        self.database_path = 'sqlite:///' + database_path
        # engine is the path that our database is stored.
        logging.debug('Generating database at: {}'.format(self.database_path))
        engine = create_engine(self.database_path)
        # metadata.create_all ensures that the table defined in GenomeEntry
        Base.metadata.create_all(engine)
        Session.configure(bind=engine)
        self.session = Session()

    def __str__(self):
        """Custom string output method for logging and printing."""
        genomes = self.get_found_genomes()
        return str([str(genome) for genome in genomes])

    def save_genome(self, **kwargs):
        """The internal function that will save a supplied genome to the
        sqlite database."""
        new_genome = GenomeEntry(**kwargs)
        self.session.merge(new_genome)  # Add the instance to the session.
        self.session.commit()  # Commit the new entry to the database/session.
        logging.info('Genome {} found and added to the database.'
                     .format(new_genome.taxonomic_name))
        return

    def get_found_genomes(self):
        """Print all the Genomes in the database to the terminal."""
        query = self.session.query(GenomeEntry).all()
        return query
