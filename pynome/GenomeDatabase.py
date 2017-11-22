# -*- coding: utf-8 -*-

import os
from pynome.GenomeAssembly import GenomeAssembly


class GenomeDatabase(object):
    """
    Base Genome Database class. 
    
    This class is not intended to be called directly but should be implemented
    via child classes.

    """
    
    def __init__(self, download_path, Storage, **kwargs):
        """
        Initialization of the GenomeDatabase class.
        
        :param download_path: 
            The path where genomes will be saved to.
        :param database_path: 
            The path where the SQLite database is located. The
            SQLite database that stores metadata about a genome assembly. If the
            SQLite file does not exist it will be created. If it does exist then
            existing data will be used.
            
        """
        self.storage = Storage
        
        # The root location where downloaded genomes will be stored.
        self.download_path = download_path  
                
        # If the download or database paths don't exist then create them.
        if not os.path.exists(self.download_path):
            os.makedirs(self.download_path)
                    
        
    def __str__(self):
        """
        Prints the list of genomes currently loaded for this genome database.
        
        """
        genomes = self.get_genomes()
        return str([str(genome) for genome in genomes])


    def save_genome(self, **kwargs):
        """
        Adds a new genome assembly or updates an existing genome assembly.
        
        :param kwargs:
         A list of key/value pairs defining the genome.  The available keys
         are
           - taxonomic_name: The taxonomic name and primary key of
             the GenomeAssembly.
           - species: The species name.
           - assembly_name: The name of the assembly.
           - genus: The genus of the assembly.
           - taxonomy_id: The numerical taxonomy identifier.
           - intraspecific_name: The intra-specific name of a given entry.
        
           - fasta_uri: The fa.gz url as a String.
           - fasta_size: The remote size of the fa.gz file as an Integer.
           - gff3_uri: The gff3.gz uri as a String.
           - gff3_size: The remote size of the gff3.gz file as an Integer.
        
           - local_path: The local path of this genome as a String.
           - base_filename: The filename base for this genome item entry.
             [genus]_[species]{_[infraspecific name]}-[assembly_name]
        
        """
        # Create a new GenomeAssembly instance, add the instance to the 
        # SQLAlchemy session and commit to the database.
        assembly = GenomeAssembly(**kwargs)
        self.storage.save_assembly(assembly)
        
        return


    def get_genomes(self):
        """
        Retrieves a list of all genomes loaded for this genome database.
        
        """
        query = self.session.query(GenomeAssembly).all()
        return query
