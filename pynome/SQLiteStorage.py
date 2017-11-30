# -*- coding: utf-8 -*-

import os
import logging
from pynome.Storage import Storage
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, create_engine

from sqlalchemy.orm import sessionmaker

Session = sessionmaker()

Base = declarative_base()


class SQLiteStorage(Storage):

    def __init__(self, **kwargs):

        # The SQLAlchemy session object.
        self.session = Session()

        # The full path where the sqlite databse is housed.
        self.database_path = kwargs['database_path']
        self.database_path = 'sqlite:///' + self.database_path

        # Create the database path if it does not exist.
        if not os.path.exists(self.database_path):
            os.makedirs(self.database_path)

        # Open the SQLAlchemy database where genome details are stored.
        logging.debug('Opening database at: {}'.format(self.database_path))
        engine = create_engine(self.database_path)
        Base.metadata.create_all(engine)
        Session.configure(bind=engine)

    def save_assembly(self, GenomeAssembly):

        args = {
            'taxonomic_name': GenomeAssembly.taxonomic_name,
            'species': GenomeAssembly.species,
            'assembly_name': GenomeAssembly.assembly_name,
            'genus': GenomeAssembly.genus,
            'taxonomy_id': GenomeAssembly.taxonomy_id,
            'intraspecific_name': GenomeAssembly.intraspecific_name,
            'fasta_uri': GenomeAssembly.fasta_uri,
            'fasta_size': GenomeAssembly.fasta_size,
            'gff3_uri': GenomeAssembly.gff3_uri,
            'gff3_size': GenomeAssembly.gff3_size,
            'local_path': GenomeAssembly.local_path,
            'base_filename': GenomeAssembly.base_filename,
        }
        record = SQLiteAssembly(args)
        self.session.merge(record)
        self.session.commit()

    def get_assemblies(self):
        pass


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
