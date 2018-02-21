"""This module contains the AssemblyStorage class.

.. module:: assemblystorage
    :platform: Unix
    :synopsis: This class handles multiple instances of AssemblyDatabase.

.. moduleauthor:: Tyler Biggs <biggstd@gmail.com>
"""

# General Python imports.
import os
import subprocess
import collections

# SQLAlchemy imports.
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Inter-package imports.
from pynome.assembly import Base
from pynome.assembly import Assembly
from pynome.sra import download_sra_json


class AssemblyStorage:
    """Models a group of AssemblyDatabase instances.

    Provides functions for interacting with those instances.
    """

    def __init__(
            self,
            sqlite_path=None,
            base_path=None,
            irods_base_path=None):
        """Initialization of the AssemblyStorage class.

        :param [sqlite_path]:
            The local path to the sqlite database used to store metadata of
            the found genome assemblies. If no value is given, this defaults
            to `"sqlite:///genomes.db"`.

        :param base_path:
            The local filepath where Pynome will save its files. If no value
            is given, the file "Genomes" will be created and used within the
            current working directory.

        :param irods_base_path:
            The base path to be used with iRODs integration.
        """

        # If the sqlite path is not give, create one in memory.
        if sqlite_path is None:
            sqlite_path = "sqlite://"

        # Otherwise, create the intermediate path, then append the
        # database filename to the class attribute.
        else:
            if not os.path.exists(sqlite_path):
                os.makedirs(sqlite_path)
            sqlite_path = os.path.join('sqlite:///' + sqlite_path, 'Genome.db')

        self.sqlite_path = sqlite_path

        # If no base_path is given, creata a folder named "Genomes" in
        # the current working directory for use as the base_path.
        if base_path is None:
            base_path = 'genomes'

        self.base_path = base_path

        # Create sub-paths for each type of file to be downloaded.
        self.base_genome_path = os.path.join(self.base_path, 'Genome')
        self.base_sra_path = os.path.join(self.base_path, 'RNA-Seq')

        # Define the public attributes of the class.
        self.sources = dict()

        # self.sqlite_session = sqlite_session
        self.irods_base_path = irods_base_path
        Session = sessionmaker()

        # Prepare the SQLite engine and session.
        self.engine = create_engine(self.sqlite_path)
        # Create the tables.
        Base.metadata.create_all(self.engine)
        self.session = Session(bind=self.engine)

    def save_assembly(self, new_assembly):
        """Save a given assembly object to the SQLite database.

        :param new_assembly:
            A pynome.Assembly object to be saved in the local sql database.
        """
        self.session.merge(new_assembly)
        self.session.commit()

    def save_assemblies(self):
        """Save a list of assembly objects to the SQLite database.
        """
        for src_name, source in self.sources.items():
            for assembly in source.assemblies:
                self.save_assembly(assembly)

    def update_assembly(self, assembly_base_filename, update_dict):
        """Update the SQLite entry of a given assembly with update_dict.

        :param assembly_base_filename:
            The base filename and primary key of an assembly.

        :param update_dict:
            A dictionary with values to update the SQLite table with.
        """
        self.session.query(Assembly).filter_by(
            base_filename=assembly_base_filename).update(update_dict)

    def query_local_assemblies(self):
        """Queries the local SQLite database, and returns a list of all
        assemblies therein.
        """
        query = self.session.query(Assembly).all()
        return query

    def query_local_assemblies_by(self, field, value):
        """Query the local SQLite database and return results filtered by the
        given column name (filter) and value.

        :param field:
            The column to be searched. Possible values: species, genus,
            intraspecific_name, assembly_id.

        :param value:
        """
        query = self.session.query(Assembly).filter(
            getattr(Assembly, field) == value).all()
        return query

    def crawl(self, assembly_database, urls=None):
        """Call the crawl function on the given assembly_database.

        This the assembly database should return something for this class
        to handle saving.
        """
        self.sources[assembly_database].crawl(urls)

    def crawl_all(self):
        """Call the crawl function on every AssemblyDatabase in sources.
        """
        for source in self.sources:
            source.crawl()

    def download(self, assemblies):
        """Download a specific set of assemblies from a given list.

        :param assemblies:
             A list of Pynome Assembly objects.
        """
        # Create a dictionary to hold assemblies from different remote sources.
        download_dict = collections.defaultdict(list)

        # Iterate through the assemblies provided and build a list for each
        # remote database source encountered.
        for ga in assemblies:

            # Get the name of the source database of the given assembly.
            source_db = ga.source_database

            # Append it to the corresponding list within download_dict.
            download_dict[source_db].append(ga)

        # Iterate through the dictionary entries.
        for src, assembly_list in download_dict.items():

            # Get the corresponding database entry from the sources dictionary.
            assembly_db = self.sources[src]

            # Use the database download function to download the assembly.
            assembly_db.download(assembly_list, self.base_genome_path)

    def download_all(self):
        """Downloads all assemblies found within each source. The assemblies
        to be downloaded must be present in the local SQLite database.

        This call to the AssemblyDatabase child class should download all
        files needed to build complete assembly metadata sets.
        """

        # For each source, find all assemblies that belong.
        for src_name, source in self.sources.items():

            src_assemblies = self.query_local_assemblies_by(
                'source_database', src_name)

            source.download(src_assemblies, self.base_genome_path)

    def download_all_sra(self):
        """
        """
        tax_ids = [gen.taxonomy_id for gen in self.query_local_assemblies()]

        download_sra_json(self.base_sra_path, tax_ids)

    def add_source(self, new_source):
        """Append a new source to the sources dictionary."""
        # Get the name attribute of this new database.
        db_name = new_source.database_name

        # Add the new database to the source dictionary using its name as a key.
        self.sources[db_name] = new_source

    def push_irods(self):
        """Pushes all the files within each source to an iRODs server.
        """
        pass

    def decompress(self, assembly):
        """Decompress (GNU Unzip) a single set of assembly files.

        :param assembly:
            An assembly object stored within the local SQLite database.
        """

        fasta_gz = os.path.join(
            self.base_genome_path,
            assembly.base_filepath,
            assembly.base_filename + '.fa.gz')

        gff3_gz = os.path.join(
            self.base_genome_path,
            assembly.base_filepath,
            assembly.base_filename + '.gff3.gz')

        cmd = ['gunzip', '-f', fasta_gz]
        subprocess.run(cmd)

        cmd = ['gunzip', '-f', gff3_gz]
        subprocess.run(cmd)

    def hisat_index(self, assembly):
        """Generate hisat2 indecies for a given assembly.

        This function calls `hisat2-build -f` from the command line.

        See the HISAT2 manual for more:
        https://ccb.jhu.edu/software/hisat2/manual.shtml#running-hisat2

        :param assembly:
            An assembly object stored within the local SQLite database.
        """

        # Construct the path to the input file.
        file_path = os.path.join(
            self.base_genome_path,
            assembly.base_filepath,
            assembly.base_filename + '.fa')

        # Construct the base filename of the output files.
        out_base = os.path.join(
            self.base_genome_path,
            assembly.base_filepath,
            assembly.base_filename)

        # Count the number of processors available to HISAT2. This value must
        # be a string for it to function within subprocess.run().
        # TODO: Make this value an option within the .json config file.
        numb_proc = str(os.cpu_count())

        cmd = ['hisat2-build', '--quiet', '-p', numb_proc,
               '-f', file_path, out_base]

        subprocess.run(cmd)

    def gtf(self, assembly):
        """Generates a `.gtf` file from a corresponding `.gff3` file.

        :param assembly:
            An assembly object stored within the local SQLite database.
        """
        gff3_file = os.path.join(
            self.base_genome_path,
            assembly.base_filepath,
            assembly.base_filename)

        cmd = ['gffread', '-T', gff3_file + '.gff3', '-o', gff3_file + '.gtf']

        subprocess.run(cmd)

    def splice_site(self, assembly):
        """Generates the splice sites of a given assembly from a `.gtf` file.

        :param assembly:
            An assembly object stored within the local SQLite database.
        """
        gft_file = os.path.join(
            self.base_genome_path,
            assembly.base_filepath,
            assembly.base_filename + '.gtf')

        splice_output = os.path.join(
            self.base_genome_path,
            assembly.base_filepath,
            assembly.base_filename + '.Splice_sites')

        with open(splice_output, 'w') as f:
            cmd = ['hisat2_extract_splice_sites.py', gft_file]

            subprocess.run(cmd, stdout=f)

    def prepare(self, assembly):
        """Prepares assembly files for downstream use."""
        self.decompress(assembly)
        self.hisat_index(assembly)
        self.gtf(assembly)
        self.splice_site(assembly)
