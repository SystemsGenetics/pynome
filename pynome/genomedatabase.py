# TODO: Write module docstring.
# TODO: Go over sqlalchemy import method. Is this the best way?
from sqlalchemy import MetaData, Table, Column, Integer, Numeric,\
    String, DateTime, ForeignKey, create_engine
from sqlalchemy.orm import sessionmaker, relationship, backref
from sqlalchemy.ext.declarative import declarative_base

"""
    Using SQLAlchemy
    ================

    To store the collected genomes on a local sqlite server.

    Must:   1. inherit from `declarative_base` object.
            2. Contain the __tablename__ to be used in the database.
            3. Contain one or more Column objects.
            4. Ensure one or more attributes are primary keys. 

"""

Base = declarative_base()
# TODO: Should this sqlalchemy stuff go here?
# TODO: If so, they should probably be denoted as private.
# engine = create_engine('sqlite:///local_genomes.db')
engine = create_engine('sqlite:///:memory:')
# engine = create_engine('sqlite://///media/tylerbiggs/genomic/PYNOME.db')
Session = sessionmaker(bind=engine)
session = Session()


class GenomeEntry(Base):  # Inherit from declarative_base.
    """
    A sqlite handler for the GenomeTable database.

    This supposedly will both create the desired sql table, as well as
    act as the handler for generating new row entries into said table.

    To add a record to the database, an instance of this class must be 
    initialized with the desired data within. Then that new instance of
    the GenomeEntry will be added to the session, and then committed.
    """
    # TODO: Consider how this class should interact with the logger.
    # TODO: Is 150 characters a reasonable limit for taxonomic names?
    # TODO: Add a download type! This assumes only one!
    #       This should probably be done by creating another table.
    __tablename__ = "GenomeTable"  # Should this be the same as the class?
    genome_taxonomic_name = Column(String(150),primary_key=True)
    download_method = Column(String(10))
    genome_fasta_uri = Column(String(1000))
    genome_gff3_uri = Column(String(1000))
    genome_local_path = Column(String(1000))
    gff3_size = Column(Integer())
    fasta_size = Column(Integer())

    def __init__(self, genome_taxonomic_name, **kwargs):
        """Contructor that overrides the default provided. This ensures that
        a genome_taxonomic_name is required for each GenomeEntry."""
        self.genome_taxonomic_name = genome_taxonomic_name
        for key, value in kwargs.items():  # Set the attributes found in **kwargs
            setattr(self, key, value)

    def __repr__(self):
        """Custom representation that will be pulled up when a print out
        is requested. This will be of the form:

        GENOME ENTRY
        ============
            __Name__:       {}
            __fasta uri__:  {}   remote size:   {}
            __gff3 uri__:   {}   remote size:   {}
            __local path__: {}

        """
        repr =  "GENOME ENTRY\n============\n\tName:\t{self.genome_taxonomic_name} \
        \n\tfasta uri:\t{self.genome_fasta_uri}\n\t\tremote size\t{self.fasta_size} \
        \n\tgff3 uri:\t{self.genome_gff3_uri}\n\t\tremote size\t{self.gff3_size} \
        \n\tlocal path:\t{self.genome_local_path}".format(self=self)
        return repr

Base.metadata.create_all(engine)  # Create all the tables defined above.
# TODO: Should this Base.metadata.create_all() function really go here?
# Or should the whole thing be wrapped in another class or module?
# Doesn't work well / obviously when placed within the GenomeDatabase class.


class GenomeDatabase(object):
    """
    @brief     Base Genome Database class.
               Many functions will have to be overwritten by
               the database-specific child classes.
    """
    
    def __init__(self):
        """
        @brief     Initialization of the GenomeDatabase class.
        """
        # Create attributes that are not related to SQLAlchemy.
        self._baseGenomeDir = None
        self._genomeList = []
        self._downloadProtocol = None

    def save_genome(self, taxonomic_name, **kwargs):
        """
        @brief     Save the genomes in this database.
                   Save to the _baseGenomeDir location.
        """
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
        session.merge(new_genome)  # Add the instance to the session.
        session.commit()  # Commit the new entry to the database/session.

    def print_genomes(self):
        """
        @brief     Print all the Genomes in the database to the terminal.
                   TODO: Implement.
        """
        query = session.query(GenomeEntry).all()
        # print(query)
        return query

    def find_genomes(self):
        """
        @brief     To be overwritten by child classes.
                   Very database specific.

        """
        pass

    def download_genomes(self):
        """
        @brief     To be overwritten by child classes.
                   Very database specific.
        """
        pass
