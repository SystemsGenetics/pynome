# -*- coding: utf-8 -*-

from pynome.GAStorage import GAStorage
from sqlalchemy import Column, Integer, String
from pynome.SQLiteGAStorage import Base


class SQLiteAssembly(Base):
    
    """
    A sqlite handler for the GenomeTable database.

    This will both create the desired sql table, as well as
    act as the handler for generating new row entries into said table.
    To add a record to the database, an instance of this class must be
    initialized with the desired data within. Then that new instance of
    the GenomeAssembly will be added to the session, and then committed.
    Each GenomeAssembly has:

    """

    # Class variables shared amongst all GenomeAssembly instances.
    
    # Define the SQLite table name.
    __tablename__ = "GenomeTable"

    # Define columns within that table.
    # TAXONOMIC ENTRIES
    taxonomic_name = Column(String(500), primary_key=True)
    species = Column(String(500))
    assembly_name = Column(String(250))
    genus = Column(String(250))
    taxonomy_id = Column(String(100))
    intraspecific_name = Column(String(100))

    # REMOTE FILES
    fasta_uri = Column(String(1000))
    fasta_size = Column(Integer())
    gff3_uri = Column(String(1000))
    gff3_size = Column(Integer())

    # LOCAL FILES
    local_path = Column(String(500))
    base_filename = Column(String(500))
    
    def __init__(self, **kwargs):
    
      # Iterater through the kwargs parameter and set the SQLAlchemy
      # table columns accordingly. 
      for key, value in kwargs.items():  
        setattr(self, key, value)
      

        
