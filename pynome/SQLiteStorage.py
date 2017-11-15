# -*- coding: utf-8 -*-

import os
import logging
from pynome.Storage import Storage
from pynome.SQLiteAssembly import SQLiteAssembly
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine

from sqlalchemy.orm import sessionmaker

# Import this in other packages with:
# >>> from pynome import Session
Session = sessionmaker()

Base = declarative_base()

class SQLiteStorage(Storage):
    
    def __init__(self, **kwargs):
        
      # The SQLAlchemy session object.
      self.session = Session()  
      
      # The full path where the sqlite databse is housed.
      self.database_path = kwargs['database_path'];
      self.database_path = 'sqlite:///' + self.database_path
      
      # Create the database path if it does not exist.
      if not os.path.exists(self.database_path):
        os.makedirs(self.database_path)
        
      # Open the SQLAlchemy database where genome details are stored.
      logging.debug('Opening database at: {}'.format(self.database_path))
      engine = create_engine(self.database_path)
      Base.metadata.create_all(engine)
      Session.configure(bind = engine)
    
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