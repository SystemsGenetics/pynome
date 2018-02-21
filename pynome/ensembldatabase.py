"""This module contains the EnsemblDatabase class.

.. module:: ensembldatabase
    :platform: Unix
    :synopsis: A child class of AssemblyDatabase that implements Ensembl
    specific functions for crawling, parsing and downloading genome
    assembly files.

.. moduleauthor:: Tyler Biggs <biggstd@gmail.com>
"""

# General Python imports.
import os
import ftplib
import itertools
import logging

# Externam package imports.
import pandas
from tqdm import tqdm

# Inter-package imports.
from pynome.assembly import Assembly
from pynome.assemblydatabase import AssemblyDatabase
from pynome.utils import crawl_ftp_dir


# pylint: disable=too-many-instance-attributes


class EnsemblDatabase(AssemblyDatabase):
    """Class to handle the crawling, parsing and downloading of
    genome assembly files from the Ensembl database.
    """

    def __init__(self, ignored_dirs, data_types, ftp_url, kingdoms,
                 release_version, bad_filenames, crawl_urls=None, **kwargs):
        """The initialization function for EnsemblDatabase.

        Calls the constructor of AssemblyDatabase, and creates
        attributes and properties specific to the Ensembl database.

        :param ignored_dirs:
            Names of directories the crawler should never enter.

        :param ftp_url:
            The base URL of the ensembl FTP server to be connected to.

        :param data_types:
            The types of data to be considered. Used in construction of
            starting url paths for the crawler. Parsers only currenlty
            support the 'gff3' and 'fasta' data types.

        :param kingdoms:
            A list of genome kingdoms to be used in the construction of
            starting url paths. Available options include ['fungi', 'metazoa',
            'plants', 'protists']

        :param release_version:
            The release version of Ensembl to be used.

        :param bad_filenames:
            A list of files to be ignored by the crawl utility.

        :param [crawl_urls]:
            An optinal list of urls. If given these will be used as starting
            points for calls to crawl().

        :param [**kwargs]:
            Remaining arguments are passed to AssemblyDatabase.
        """

        # Call the parent constructor / __init__ function, pass keywords
        # to the parent constructor.
        super().__init__(**kwargs)

        # Define public attributes of the class.
        self.ftp = ftplib.FTP()
        self.ignored_dirs = ignored_dirs
        self.ftp_url = ftp_url
        self.data_types = data_types
        self.kingdoms = kingdoms
        self.release_version = release_version
        self.bad_filenames = bad_filenames
        self.crawl_urls = crawl_urls
        self.assemblies = list()

        # Define private attributes of the class.
        self.metadata_df = None
        self.database_name = 'ensembl'

    @property
    def metadata_uri(self):
        """Getter function for the metadata_uri property.

        Builds the sub-directory of the Ensembl FTP server wherein the
        species.txt metadata file can be found.
        """
        return '/'.join(('/pub', self.release_version, 'species.txt'))

    @property
    def top_dirs(self):
        """Getter function for the top_dirs property.

        Builds a list of URIs that will act as the starting points for the
        crawling function.
        """

        # Create the list to be output.
        uri_list = list()

        # Generate the ordered pairs of datatypes and kingdoms.
        datatype_kingdom_pairs = itertools.product(
            self.data_types, self.kingdoms)

        # For each pair, generate the corresponding URI.
        for datatype, kingdom in datatype_kingdom_pairs:
            uri = '/'.join(('pub', kingdom, self.release_version, datatype, ''))
            uri_list.append(uri)

        # Return the list of uris.
        return uri_list

    def ensembl_file_parser(self, line, top_dir):
        """Examines a line and add creates a GenomeAssembly if appropriate.

        This function parses one 'line' at a time retrieved from an
        ``ftp.dir()`` command. This line has already been confirmed to
        not be a directory.

        :param line:
            An input line, described in detail below.

        :param top_dir:
            The parent directory.

        :param bad_dirs:
            A list of words / strings. Files found with these terms in
            them will be rejected by the parser.
        """

        # Parse the line.
        parsed_line = self.parse_ensembl_dir_line(line)

        # If the parse_ensembl_dir_line returns None, do not examine
        # the listing.
        if parsed_line is None:
            return

        # If the filename contains a 'bad word', we should exit the function.
        if any(bw in parsed_line['file_name'] for bw in self.bad_filenames):
            # This means that one of the undesired files has been located.
            return

        # Examine the parsed output to determine if a GenomeAssembly object
        # should be created. Create a dictinoary of kwargs and filter off
        # any values of 'None', then use this dictinoaryto create a
        # new Assembly instance.
        if parsed_line['file_name'].endswith('.dna.toplevel.fa.gz'):
            # Then this file is a fasta file.

            # Remove the trailing filename from the file_name.
            # Create the corresponding argument dictionary.
            new_assembly_kwargs = {
                'source_database': self.database_name,
                'species': parsed_line['species'],
                'genus': parsed_line['genus'],
                'intraspecific_name': parsed_line['intraspecific_name'],
                'assembly_id': parsed_line['assebly_name'].replace(
                    '.dna.toplevel.fa.gz', ''),
                'version': self.release_version,
                'fasta_remote_path': ''.join((
                    top_dir, parsed_line['file_name'])),
                'fasta_remote_size': parsed_line['file_size']}

            # Create the new Assembly object.
            new_genome_assembly = Assembly(**new_assembly_kwargs)

            # Append it to the assemblies list, which is defined in the
            # AssemblyDatabase parent class.
            self.assemblies.append(new_genome_assembly)

            # Exit the if loop.
            return

        elif parsed_line['file_name'].endswith('.gff3.gz'):
            # Then this file is a gff3 file.
            # Split by periods to remove the version and file extension.
            assembly_id = parsed_line['assebly_name'].rsplit('.', 3)

            new_assembly_kwargs = {
                'source_database': self.database_name,
                'species': parsed_line['species'],
                'genus': parsed_line['genus'],
                'intraspecific_name': parsed_line['intraspecific_name'],
                'assembly_id': assembly_id[0],
                'version': self.release_version,
                'gff3_remote_path': ''.join((
                    top_dir, parsed_line['file_name'])),
                'gff3_remote_size': parsed_line['file_size']}

            # Create the new Assembly object.
            new_genome_assembly = Assembly(**new_assembly_kwargs)

            # Append it to the assemblies list, which is defined in the
            # AssemblyDatabase parent class.
            self.assemblies.append(new_genome_assembly)

            # Exit the if loop.
            return

    def parse_ensembl_dir_line(self, in_line):
        """Parse an individual line item from an ftp.dir() call.

        This function splits a line retrieved from the ensembl ftp server
        from a call to ftp.dir().

        :param in_line:
            A filename (string). This function assumes these strings are from
            the Ensembl database, and parses them appropriately.

        :returns:
            A dictionary of keywords that can be used in the construction of a
            GenomeAssembly object.


        An example line, and its index locations, are shown below::

            ``"drwxr-sr-x  2 ftp   ftp    4096 Jan 13  2015 filename"
               [0]        [1][2]   [3]    [4]  [5] [6] [7]  [8] or [-1]``

        Parses a filename to retrieve the species, assembly, version and other
        information needed to greate a new instance of GenomeAssembly.

        The filenames themselves are assumed to be either gff3 or fasta files.
        Examples of these files, extracted from README files, are shown below.

        gff3 files::

            ``<species>.<assembly>.<_version>.gff3.gz``

        fasta files::

            ``<species>.<assembly>.<sequence type>.<id type>.<id>.fa.gz``
        """

        # Split the input string by whitespace.
        dir_list = in_line.split()

        # Pull needed information out of this list. It is always the last item.
        file_name = dir_list[-1]
        file_size = dir_list[4]

        # If the filename contains a 'bad word', we should exit the function.
        if any(bw in file_name for bw in self.bad_filenames):
            # This means that one of the undesired files has been located.
            return

        logging.debug(f'parsing the line: {in_line}')

        # Split the file_name by the first two '.'.
        # This will give a string that contains the genus and species
        # informaiton, and a string that contains the assembly name.
        try:
            name_list = file_name.split('.', 2)
            genus_species, assembly_name = name_list[0], name_list[1]
        except:
            logging.warning(f'Unable to parse {file_name}')
            return

        # Begin the parsing of the genus_species string. These strings can be
        # further split by intraspecific names and identifiers.
        try:

            # Split the genus and species by underscores.
            gen_species_list = genus_species.split('_')

            # Some entries have leading underscores -- this caueses 'None' to
            # appear in the list. 'None' entries must be removed.
            gen_species_list = list(filter(None, gen_species_list))

            genus = gen_species_list[0]
            species = gen_species_list[1]


            # If the length of gen_species_list is greater than 2, an
            # intraspecific name is present.
            if len(gen_species_list) > 2:

                # intraspecific name is present, and should be the third
                # element in the list to the end of the list.
                intraspecific_name = '_'.join(gen_species_list[2:])

            # Otherwise there is no intraspecific name.
            else:

                # Set intraspecific_name to None.
                intraspecific_name = None

                # Get the genus and species from the gen_species_list.
                # Since there is no intraspecific name, split the list once.
                # genus, species = genus_species.split('_', 1)

        except Exception as error:
            print('Unable to parse ensembl ftp filename.', error)

        # Return the dictionary of values parsed from the directory listing.
        return {
            'genus': genus,
            'assebly_name': assembly_name,
            'species': species,
            'intraspecific_name': intraspecific_name,
            'file_name': file_name,
            'file_size': file_size,
        }

    def crawl(self, uri_list=None):
        """
        """
        # If no uri_list is provided, set it to the class property.
        if uri_list is None:
            uri_list = self.top_dirs

        # Connect to the FTP server and login with anonymous credentials.
        self.ftp.connect(self.ftp_url)
        self.ftp.login()

        # Start a crawl at each uri.
        for uri in tqdm(uri_list, desc='Crawling. This make take some time.'):
            crawl_ftp_dir(
                ftp=self.ftp,
                top_dir=uri,
                parsing_function=self.ensembl_file_parser,
                ignored_dirs=self.ignored_dirs,
            )

        # Close the FTP connection.
        self.ftp.quit()

    def download_metadata(self, base_path=None):
        """
        """
        if base_path is None:
            base_path = os.path.join(os.getcwd(), 'genomes')

        # Build the path to the local file.
        target_file = os.path.join(base_path, 'species.txt')

        # Check if the file already exists, and that it is not 0 bytes.
        if os.path.isfile(target_file) and os.path.getsize(target_file) > 0:
            # Then the file is already there, and we can quit this function
            # early. We still need to read the csv to get the dataframe.
            self.metadata_df = pandas.read_csv(
                filepath_or_buffer=target_file,
                error_bad_lines=False,
                sep="\t",
                index_col=False)
            return

        # Connect to the FTP server and login with anonymous credentials.
        # TODO: Change the FTP connection to use a context manager, then
        # refactor this function so that progress bars can be more easily
        # implemented by the cli.
        self.ftp.connect(self.ftp_url)
        self.ftp.login()

        # size_estimate = self.ftp.size(self.metadata_uri)

        self.ftp.retrbinary(
            cmd='RETR {}'.format(self.metadata_uri),
            callback=open(target_file, 'wb').write
        )

        # Close the FTP connection.
        self.ftp.quit()

        # Read the species.txt metadata file, and assign it to a dataframe
        # attribute of the EnsemblDatabase class.
        self.metadata_df = pandas.read_csv(
            filepath_or_buffer=target_file,
            error_bad_lines=False,
            sep="\t",
            index_col=False)

    def download(self, assemblies, base_path=None):
        """
        """
        # TODO: Consider how this function is called from AssemblyStorage.
        # If a base_path is not given, create a folder called 'genomes',
        # and place it in the current directory.
        if base_path is None:
            base_path = os.path.join(os.getcwd(), 'genomes')

        # Connect to the FTP server and login with anonymous credentials.
        self.ftp.connect(self.ftp_url)
        self.ftp.login()

        for gen in tqdm(assemblies, desc='Downloading Assemblies...'):

            # Create the base_path for this genome assembly.
            curr_base_path = os.path.join(base_path, gen.base_filepath)

            # Create the intermediary folders if they do not exist.
            if not os.path.exists(curr_base_path):
                os.makedirs(curr_base_path)

            # Create the local filenames.
            new_gff3 = os.path.join(
                curr_base_path,
                gen.base_filename + '.gff3.gz')

            new_fasta = os.path.join(
                curr_base_path,
                gen.base_filename + '.fa.gz')

            # Download the desired files.
            self.ftp.retrbinary(
                cmd=f'RETR {gen.fasta_remote_path}',
                callback=open(new_fasta, 'wb').write)

            self.ftp.retrbinary(
                cmd=f'RETR {gen.gff3_remote_path}',
                callback=open(new_gff3, 'wb').write)

        # Close the FTP connection.
        self.ftp.quit()

    def find_taxonomy_id(self, tax_name):
        """Searches the self.metadata_df attribute for a matching taxonomy ID.

        :param tax_name:
            A string representing the taxonomic name of an assembly.

        :returns:
            A string of the found taxnomy ID, or `None`.
        """

        # Search the pandas dataframe with the metadata parsed from species.txt.
        taxonomy_id = self.metadata_df[
            self.metadata_df['species'].str.match(
                tax_name.lower())]['taxonomy_id'].values

        # Check if this actually found a value, if it did not, log the failure.
        if taxonomy_id.size == 0:
            logging.warning(
                'Unable to find a taxonomy id for {}'.format(tax_name))
            return None

        return str(taxonomy_id[0])

    def add_taxonomy_ids(self, assemblies=None):
        """Calls `find_taxonomy_id` on a list of assemblies, and returns a list
        of tuples containing the base_filename and an update dictionary.

        :param [assemblies=None]:
            If no list of assembly objects is given, the contents of
            self.assemblies is used instead.

        :returns:
            A list of tuples, containing the assemblies base filename and an
            update dictionary containing the newly found taxnomy_ID.
        """
        # Output list holder.
        tax_update_list = list()

        # Iterate through the list of assemblies, if none are provided, use
        # those found in the self.assemblies list.
        if assemblies is None:
            assemblies = self.assemblies

        for gen in assemblies:

            # Search the metadata dataframe for a matching entry.
            tax_id = self.find_taxonomy_id(gen.taxonomy_name)

            # If `None` is returned from self.find_taxonomy_id, continue
            # with the loop without creating an update dictionary.
            if tax_id is None:
                continue

            # Otherwise, create the update dictionary and append it to the
            # output list.
            update_dict = {'taxonomy_id': tax_id}
            tax_update_list.append(
                (gen.base_filename, update_dict))

        return tax_update_list
