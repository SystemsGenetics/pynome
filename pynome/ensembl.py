"""
================
Ensembl Database
================

The ensembl database module. A child class of the genome database class,
this module cotains all code directly related to connecting and parsing data
from the ensembl geneome database."""

import ftplib
import os
import logging
import itertools
from pynome.database import GenomeDatabase
from pynome.ftpHelper import crawl_ftp_dir
from tqdm import tqdm

ENSEMBL_FTP_URI = 'ftp.ensemblgenomes.org'
ENSEMBL_DATA_TYPES = ['gff3', 'fasta']
ENSEMBL_KINGDOMS = ['fungi', 'metazoa', 'plants', 'protists']


class EnsemblDatabase(GenomeDatabase):
    """The EnsemblDatabase class. This handles finding and downloading
    genomes from the ensembl genome database. The database url is:

        ```ftp.ensemblgenomes.org```

    It does so by recursively walking the ftp directory. It only collects
    those genomes that have a ``*.gff3.gz`` or a ``*.fa.gz`` file.
    """

    def __init__(self, release_version=36, **kwargs):
        super().__init__(**kwargs)  # Call parent class init
        self._release_version = None  # set by the release version setter
        self._release_number = None  # set by the release version setter
        self.release_version = release_version
        self.ftp = ftplib.FTP()  # the ftp instance for the database

    @property
    def release_version(self):
        """Release version property. Should be in the form:
            ``"release-#", "release-36"``"""
        return self._release_version

    @release_version.setter
    def release_version(self, value):
        """Setter for the release_version. Accepts an input integer and returns
        a string in the form: 'release-##' """
        self._release_number = value
        self._release_version = 'release-' + str(value)

    def generate_metadata_uri(self):
        """Generates a URI that will locate the metadata. This URI is of the
        form:

        ``/pub/release-36/species.txt``
        """
        uri_dict = {}
        species_txt = 'species.txt'
        uri = '/'.join(('pub', self._release_version, species_txt))
        uri_dict[uri] = species_txt
        return uri_dict

    def download_metadata(self):
        """Downloads the 'species_EnsemblKINGDOM.txt files. These are smaller, more
        usable metadata file found in each """

        metadata_uri_dict = self.generate_metadata_uri()

        self.ftp.connect(ENSEMBL_FTP_URI)
        self.ftp.login()

        for uri, file_name in metadata_uri_dict.items():

            size_estimate = self.ftp.size(uri) / 8.192
            target_dir = os.path.join(self.download_path, file_name)

            with tqdm(total=int(size_estimate), unit_scale=True,
                      unit='MB') as meta_pbar:

                with open(target_dir, 'wb') as curr_file:

                    def callback(data):
                        update_size = len(data) / 8.192
                        meta_pbar.update(int(update_size))
                        curr_file.write(data)

                    try:
                        self.ftp.retrbinary(
                            cmd='RETR {}'.format(uri),
                            callback=callback)
                    except:
                        logging.warning('UNABLE TO DOWNLOAD METADATA!')
        return

    def generate_uri(self):
        """Generates the uri strings needed to download the genomes
        from the ensembl database.

        **Returns**: List of Strings of URIs for the ensembl database. eg::

            'pub/fungi/release-36/gff3/',
            'pub/metazoa/release-36/gff3/',
            ...

        This is an extremely case-specific function."""
        uri_list = []
        # Unique permutations of data types and kingdoms.
        uri_gen = itertools.product(ENSEMBL_DATA_TYPES, ENSEMBL_KINGDOMS)
        # For each iteration, return the desired URI.
        for item in uri_gen:
            uri = '/'.join(('pub', item[1],  # the clade or kingdom
                            self._release_version,
                            item[0], '',))  # the data type
            uri_list.append(uri)
        return uri_list

    def ensembl_line_parser(self, line, top_dir):
        """This function parses one 'line' at a time retrieved from an
        ``ftp.dir()`` command. This line has already been confirmed to
        not be a directory.

        :param top_dir: The parent directory.
        :param line: An input line, described in detail below.

        An example of one such line:

            ``"drwxr-sr-x  2 ftp   ftp    4096 Jan 13  2015 filename"``

        The files are consistently named following this pattern:

            ``<species>.<assembly>.<_version>.gff3.gz``

        This line is split by whitespace. For future reference, the indexes
        correspond (usually) to::

            + ``[0]:    the directory information.``
            + ``[1]:    the number of items therein?``
            + ``[2]:    unknown always 'ftp'``
            + ``[3]:    unknown always 'ftp'``
            + ``[4]:    the file size in bytes, 4096 is one block``
            + ``[5]:    Month``
            + ``[6]:    Day``
            + ``[7]:    Year``
            + ``[8]:    filename``

        Either adds a genome, or returns nothing."""

        bad_words = ('chromosome', 'abinitio')

        def split_line(line):
            """Parse an individual item line from an ftp.dir() call.
            This function handles splitting, without assuming the line
            contains a valid genome file."""
            item = line.split()   # Split the listing by whitespace.
            line_dict = {
                'dir_info': item[0],
                'dir_subfolders': item[1],
                'size': item[4],
                'item_name': item[-1]
            }
            return line_dict

        def parse_genome_name(line_dict):
            """Takes an item line dictionary and splits the genomes name
            to get the desired values from it."""
            name_list = line_dict['item_name'].split('.', 2)
            genus_species = name_list[0]
            assembly_name = name_list[1]
            genus, species = genus_species.split('_', 1)
            # parsed_name = genus + '_' + species + '-' + assembly_name
            return {
                'taxonomic_name': genus_species,
                'genus': genus,
                'assembly_name': assembly_name,
                'species': species}

        def add_fasta(line_dict):
            fasta_genome = parse_genome_name(line_dict)
            update_dict = {
                'fasta_size': line_dict['size'],
                'fasta_uri': ''.join((top_dir, line_dict['item_name'])),
            }
            fasta_genome.update(update_dict)
            self.save_genome(**fasta_genome)
            return

        def add_gff3(line_dict):
            gff3_genome = parse_genome_name(line_dict)
            update_dict = {
                'gff3_size': line_dict['size'],
                'gff3_uri': ''.join((top_dir, line_dict['item_name'])),
            }
            gff3_genome.update(update_dict)
            self.save_genome(**gff3_genome)
            return

        line_dict = split_line(line)

        if any(bw in line_dict['item_name'] for bw in bad_words):
            # This means that one of the undesired files has been located.
            return

        elif line_dict['item_name'].endswith('dna.toplevel.fa.gz'):
            add_fasta(line_dict)
            return

        elif line_dict['item_name'].endswith('gff3.gz'):
            add_gff3(line_dict)
            return

    def find_genomes(self, uri_list, parsing_function=ensembl_line_parser):
        """Private function that handles finding the list of genomes.

        :param parsing_function: This should be a function that reads an
            ``ftplib.dir()`` line output. This output should always be a
            file, not a directory.
        :param uri_list: This should be a list of base URIs to start
            the ftp crawler from."""
        self.ftp.connect(ENSEMBL_FTP_URI)  # connect to the ensemble ftp
        self.ftp.login()
        for uri in tqdm(uri_list):
            # logging.info('Parent crawl dir initialized as: {}'.format(uri))
            crawl_ftp_dir(
                database=self,
                top_dir=uri,
                parsing_function=parsing_function)
        self.ftp.quit()  # close the ftp connection
        return

    def estimate_download_size(self):
        size = []
        genomes = self.get_found_genomes()
        for genome in genomes:
            size.extend((
                genome.gff3_size,
                genome.fasta_size
            ))
        return sum(filter(None, size))

    def download_genomes(self):
        """This function takes an list of genome tuples.
        The directory structure to fit the files downloaded is as follows::

            Genome/
              [genus]_[species]{_[intraspecific_name]}/
                [assembly_name]/
                  [genus]_[species]{_[intraspecific_name]}-[assembly_name].gff3
                  [genus]_[species]{_[intraspecific_name]}-[assembly_name].fasta

        """
        size_estimate = self.estimate_download_size() / 8.192
        genomes = self.get_found_genomes()
        self.ftp.connect(ENSEMBL_FTP_URI)
        self.ftp.login()

        with tqdm(total=int(size_estimate), unit_scale=True,
                  unit='MB') as total_pbar:
            # Iterate through the list of acquired genomes.
            for genome in genomes:
                # Create a dictionary. This is kind of awkward.
                download_dict = {
                    genome.fasta_uri: 'fa.gz',
                    genome.gff3_uri: 'gff3.gz',
                }
                # Create the target directory.
                target_dir = os.path.join(
                    self.download_path,
                    genome.genus,
                    genome.taxonomic_name
                )
                if not os.path.exists(target_dir):
                    os.makedirs(target_dir)

                # Iterate through the download dictionary
                for uri, file_ext in download_dict.items():
                    target_file = target_dir + file_ext
                    with open(target_file, 'wb') as curr_file:

                        def callback(data):
                            update_size = len(data) / 8.192
                            total_pbar.update(int(update_size))
                            curr_file.write(data)

                        try:
                            self.ftp.retrbinary(
                                cmd='RETR {}'.format(uri),
                                callback=callback)
                        except:
                            logging.warning('UNABLE TO DOWNLOAD A GENOME')
                            logging.warning(genome.taxonomic_name)

        self.ftp.quit()  # close the ftp connection
        return
