"""
**************
Genomedatabase
**************

The **Genomedatabase** module consists of two classes:

    + :class:`GenomeEntry` - An ``sql declarative_base()`` instance.
    + :class:`GenomeDatabase` - The handler for above, and the parent\
        class for specific databases to be overloaded."""

from sqlalchemy import MetaData, Table, Column, Integer, Numeric,\
    String, DateTime, ForeignKey, create_engine
from sqlalchemy.orm import sessionmaker, relationship, backref
from sqlalchemy.ext.declarative import declarative_base

# Inherit from declarative_base()
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
    
    """
    __tablename__ = "GenomeTable"  # Should this be the same as the class?
    taxonomic_name = Column(String(150),primary_key=True)
    download_method = Column(String(10))
    fasta_uri = Column(String(1000))
    gff3_uri = Column(String(1000))
    genome_local_path = Column(String(1000))
    gff3_size = Column(Integer())
    fasta_size = Column(Integer())

    def __init__(self, taxonomic_name, **kwargs):
        """Contructor that overrides the default provided. This ensures that
        a taxonomic_name is required for each GenomeEntry."""
        self.taxonomic_name = taxonomic_name
        for key, value in kwargs.items():  # Set the attributes found in **kwargs
            setattr(self, key, value)

    def __repr__(self):
        """Custom representation that will be pulled up when a print out
        is requested. This will be of the form:

        **Name**:       {}
        **fasta uri**:  {}   remote size:   {}
        **gff3 uri**:   {}   remote size:   {}
        **local path**: {}

        """
        repr =  "\n\tName:\t{self.taxonomic_name} \
        \n\tfasta uri:\t{self.fasta_uri}\n\t\tremote size\t{self.fasta_size} \
        \n\tgff3 uri:\t{self.gff3_uri}\n\t\tremote size\t{self.gff3_size} \
        \n\tlocal path:\t{self.genome_local_path}\n".format(self=self)
        return repr


class GenomeDatabase(object):
    """Base Genome Database class. Many functions will be overwritten by
    the database-specific child classes.

    .. warning:: **This class should not be directly called.**
        It must be implemented with a child class to fill out certain
        functions."""
    
    def __init__(self, engine):
        """Initialization of the GenomeDatabase class."""
        # Create attributes that are not related to SQLAlchemy.
        Session = sessionmaker(bind=engine)
        self.engine = engine
        self.session = Session()
        self._baseGenomeDir = None  # The local download location.

    def save_genome(self, taxonomic_name, **kwargs):
        """Save the genomes in this database. Save to the _baseGenomeDir
         location."""
        # Call the internal addition function.
        # TODO: Examine SQLAlchemy, there is a specific function to use
        #       for storing one vs many database entries.
        # TODO: Check to see if the genome exists already if so update
        #       it with any new information retrieved.

        self._save_genome(taxonomic_name, **kwargs)
        return
    
    def _save_genome(self, taxonomic_name, **kwargs):
        """The internal function that will save a supplied genome to the
        sqlite database."""
        new_genome = GenomeEntry(taxonomic_name, **kwargs)
        # TODO: Ensure that **kwargs passes the dictionary of attributes.
        self.session.merge(new_genome)  # Add the instance to the session.
        self.session.commit()  # Commit the new entry to the database/session.

    def print_genomes(self):
        """Print all the Genomes in the database to the terminal."""
        query = self.session.query(GenomeEntry).all()
        return query

    def find_genomes(self):
        """To be overwritten by child classes. Very database specific."""
        pass

    def download_genomes(self):
        """To be overwritten by child classes. Very database specific."""
        pass
