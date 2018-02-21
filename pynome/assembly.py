"""This module contains the Assembly class used to model genome assemblies.

.. module:: assembly
    :platform: Unix
    :synopsis:

.. moduleauthors:: Tyler Biggs <biggstd@gmail.com>
"""

# Import general python packages.
import os
import logging

# SQLAlchemy imports.
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.hybrid import hybrid_property

# Create the declarative base class.
Base = declarative_base()


class Assembly(Base):
    """Models a genome assembly for use by Pynome.

    Prepares identifier strings and filepaths based on its attributes. Also
    contains functions to prepare the assembly files (fasta and gff3) for
    use by creating a `.gff` file, finding splice sites, and creating an
    index with `hisat2`.
    """

    # Declare the SQLite table name to be used.
    __tablename__ = 'Assemblies'

    # Declare public attributes, and assign them to the class instance.
    # Columns declared in this way can be accessed as if they were
    # self.column_name, that is, the same as other attributes.
    base_filename = Column(String, primary_key=True)
    base_filepath = Column(String)
    species = Column(String)
    genus = Column(String)
    intraspecific_name = Column(String)
    assembly_id = Column(String)
    version = Column(String)
    gff3_remote_path = Column(String)
    gff3_remote_size = Column(Integer)
    fasta_remote_path = Column(String)
    fasta_remote_size = Column(Integer)
    taxonomy_name = Column(String)
    taxonomy_id = Column(String)
    source_database = Column(String)

    def __init__(self, species, genus, assembly_id, intraspecific_name=None,
                 **kwargs):
        """Initialization of the Assembly model class. Builds the primary
        key to be used by the SQLite database.

        :param species:
            The species name as a string.

        :param genus:
            The genus name as a string.

        :param assembly_id:
            The assembly identifier, as labeled from the assembly file source.

        :param [intraspecific_name]:
            An intraspecific name of the species.
        """
        self.species = species
        self.genus = genus
        self.assembly_id = assembly_id
        self.intraspecific_name = intraspecific_name
        self.base_filename = None

        if intraspecific_name is not None:
            name = '_'.join((
                self.genus,
                self.species,
                self.intraspecific_name))

        else:
            name = '_'.join((self.genus, self.species))

        self.base_filename = '-'.join((name, self.assembly_id))
        self.taxonomy_name = name

        self.base_filepath = os.path.join(name, self.assembly_id)
        # logging.warning(f'base filepath: {self.base_filepath}')

        # Iterater through the kwargs parameter and set the SQLAlchemy
        # table columns accordingly.
        for key, value in kwargs.items():
            setattr(self, key, value)

    def __repr__(self):
        """The string representation of an Assembly object.
        """
        out_str = (
            '\n'
            f'Base filename:         {self.base_filename}\n'
            f'Base filepath:         {self.base_filepath}\n'
            f'Species:               {self.species}\n'
            f'Genus:                 {self.genus}\n'
            f'Intraspecific Name:    {self.intraspecific_name}\n'
            f'Assembly ID:           {self.assembly_id}\n'
            f'Version:               {self.version}\n'
            f'gff3 URI:              {self.gff3_remote_path}\n'
            f'gff3 remote size:      {self.gff3_remote_size}\n'
            f'fasta URI:             {self.fasta_remote_path}\n'
            f'fasta remote size:     {self.fasta_remote_size}\n'
            f'Taxonomy ID:           {self.taxonomy_id}\n'
            f'Source Database:       {self.source_database}\n'
        )
        return out_str
