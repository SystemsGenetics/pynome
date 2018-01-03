# -*- coding: utf-8 -*-

import os
# import logging

# from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import (
    Table,
    Column,
    Integer,
    String,
    # create_engine,
    MetaData
)
from sqlalchemy.orm import mapper
# from sqlalchemy.orm import sessionmaker

from pynome.storage import Storage
from pynome.genomeassembly import GenomeAssembly

# Session = sessionmaker()
# Base = declarative_base()


class SQLiteStorage(Storage):
    """
    An implementation of the Storage class for an SQLite database.

    This class holds any information needed for the operation of
    the SQLite database. It also must provide functions for saving
    instances of GenomeAssembly.

    Upon initialization this will create the defined tables.

    TODO: Ensure this is the correct way to go about this... Many
    examples have these definitions outside classes.
    """

    def __init__(self, **kwargs):
        """
        Initialize the SQLiteStorage function. Assumes the path to
        the database exists, and will exit with an error if it does
        not.
        """

        # The full path where the sqlite databse is housed.
        self.database_path = kwargs['database_path']

        # Create the database path if it does not exist.
        if not os.path.exists(self.database_path):
            os.makedirs(self.database_path)

        # Convert the database_path to include an sqlite prefix.
        self.database_path = 'sqlite:///{0}'.format(
            os.path.abspath(self.database_path))

        # Decalre the sqlalchemy MetaData table. This is a catalog
        # of Table objects with optional information concerning the
        # engine and the connection. These tables can be accessed
        # via a dictionary, eg. MetaData.tables.
        metadata = MetaData()

        # Create the tables to be used.
        GenomeAssemblyTable = Table(
            # Define the name of this SQL table.
            name='GenomeAssemblies',
            # Assign the metadata instance.
            metadata=metadata,
            # Basic genome assembly columns.
            Column('taxonomic_name', String(500), primary_key=True),
            Column('species', String(250)),
            Column('assembly_name', String(250)),
            Column('genus', String(250)),
            Column('taxonomy_id', String(250)),
            Column('intraspecific_name', String(250)),
            # Remote information.
            Column('fasta_uri', String(1000)),
            Column('fasta_size', Integer()),
            Column('gff3_uri', String(1000)),
            Column('gff3_size', Integer()),
            # Local file / storage information.
            Column('local_path', String(1000)),
            Column('base_filename', String(1000))
        )

        # Create an SQLAlchemy engine.
        # An SQLAlchemy engine is a common interface to a given database.
        # From the connection string proviced, the database type (Postgres,
        # or MySQL, etc.) and the databases location are collected.
        engine = create_engine(self.database_path)

        # Create all tables that do not already exist. This will not attempt
        # to re-create tables that already exist in the database. It is safe
        # to run multiple times, and will not delete existing data.
        metadata.create_all(engine)

    def save_assembly(self, genome_assembly):

        args = {
            'taxonomic_name': genome_assembly.taxonomic_name,
            'species': genome_assembly.species,
            'assembly_name': genome_assembly.assembly_name,
            'genus': genome_assembly.genus,
            'taxonomy_id': genome_assembly.taxonomy_id,
            'intraspecific_name': genome_assembly.intraspecific_name,
            'fasta_uri': genome_assembly.fasta_uri,
            'fasta_size': genome_assembly.fasta_size,
            'gff3_uri': genome_assembly.gff3_uri,
            'gff3_size': genome_assembly.gff3_size,
            'local_path': genome_assembly.local_path,
            'base_filename': genome_assembly.base_filename,
        }
        # record = SQLiteAssembly(args)
        self.session.merge(record)
        self.session.commit()

    def get_assemblies(self):
        pass



# class SQLiteAssembly(Base):

#     """
#     A sqlite handler for the GenomeTable database.

#     This will both create the desired sql table, as well as
#     act as the handler for generating new row entries into said table.
#     To add a record to the database, an instance of this class must be
#     initialized with the desired data within. Then that new instance of
#     the GenomeAssembly will be added to the session, and then committed.
#     Each GenomeAssembly has:

#     """

#     # Class variables shared amongst all GenomeAssembly instances.

#     # Define the SQLite table name.
#     __tablename__ = "GenomeTable"

#     # Define columns within that table.
#     # TAXONOMIC ENTRIES
#     taxonomic_name = Column(String(500), primary_key=True)
#     species = Column(String(500))
#     assembly_name = Column(String(250))
#     genus = Column(String(250))
#     taxonomy_id = Column(String(100))
#     intraspecific_name = Column(String(100))

#     # REMOTE FILES
#     fasta_uri = Column(String(1000))
#     fasta_size = Column(Integer())
#     gff3_uri = Column(String(1000))
#     gff3_size = Column(Integer())

#     # LOCAL FILES
#     local_path = Column(String(500))
#     base_filename = Column(String(500))

#     def __init__(self, **kwargs):

#         # Iterater through the kwargs parameter and set the SQLAlchemy
#         # table columns accordingly.
#         for key, value in kwargs.items():
#             setattr(self, key, value)
