"""
================
Ensembl Database
================
:Author: Tyler Biggs <tyler.biggs@wsu.edu>
:Date: July 2017

.. NOTE:: Under construction.

The ensembl database module. A child class of the genome database class,
this module cotains all code directly related to connecting and parsing data
from the ensembl geneome database."""

__docformat__ = 'reStructuredText'  # Set the formatting for the documentation

import itertools
import os
from ftplib import FTP
from sqlalchemy import select
import logging
import logging.config
from pynome.genomedatabase import GenomeDatabase, GenomeEntry



ensebml_ftp_uri = 'ftp.ensemblgenomes.org'


class EnsemblDatabase(GenomeDatabase):
    """The EnsemblDatabase class. This handles finding and downloading
    genomes from the ensembl genome database. The database url is:

        ``ftp.ensemblgenomes.org``
    
    It does so by recursively walking the ftp directory. It only collects
    those genomes that have a ``*.gff3.gz`` or a ``*.fa.gz`` file.

    :Example:

    Instructions on how to use this script.

        >>> database = EnsemblDatabase()  # Initialize a database.
 
    .. seealso:: :class:`GenomeDatabase`
    """

    def __init__(self, engine, release_version=36):
        super(EnsemblDatabase, self).__init__(engine)  # Call parent class init
        self._release_number = None  # set by the release version setter
        self.release_version = release_version
        self._ftp_genomes = []
        self.ftp = FTP()  # the ftp instance for the database
        # logging.config.fileConfig('pynome/pynomeLog.conf')
        self.logger = logging.getLogger(__name__)

    def crawl_dir(self, top_dir, parsing_function):
        """Recursively crawl a target directory. Takes as an input a
        target directory and a parsing function. The ftplib.FTP.dir()
        function is used to retrieve a directory listing, line by line,
        in string format. These are appended to a newly generated list.
        Each item in this list is subject to the parsing function.

        :param top_dir: The directory from which contents will be retrieved.
        :param parsing_function: The function to parse each result."""
        # TODO: Investigate how to turn this into a yield based function.
        retrived_dir_list = []  # empty list to hold the callback
        self.ftp.dir(top_dir, retrived_dir_list.append)
        logging.debug('crawl_dir() called with:\n\ttopdir:\t{}'\
                      .format(top_dir))
        logging.debug('crawl_dir() call retrieved:\n{}'\
            .format(retrived_dir_list))
        for line in retrived_dir_list:
            if self.dir_check(line):
                # Then the line is a directory and should be crawled.
                target_dir = ''.join((top_dir, line.split()[-1], '/'))
                self.crawl_dir(target_dir, parsing_function)
            else:  # otherwise the line must be parsed.
                parsing_function(line, top_dir)
        return

    def ensemblLineParser(self, line, top_dir):
        """This function parses one 'line' at a time retrieved from an 
        ``ftp.dir()`` command. 
        
        :param line: an input line, described in detail below.
        
        An example of one such line:

            ``"drwxr-sr-x  2 ftp   ftp    4096 Jan 13  2015 filename"``

        This line is split by whitespace. For future reference, the indexes
        correspond (usually) to::

            + ``[0]:    the directory information.``
            + ``[1]:    the number of items therein?``
            + ``[2]:    unknown always 'ftp'``
            + ``[3]:    unknown always 'ftp'``
            + ``[4]:    the filesize in bytes, 4096 is one block``
            + ``[5]:    Month``
            + ``[6]:    Day``
            + ``[7]:    Year``
            + ``[8]:    filename``
        
        Either adds a genome, or returns nothing."""
        item = line.split()   # Split the listing by whitespace.
        line_dict = {
            'dir_info' :       item[0],
            'dir_subfolders' : item[1],
            'size' :           item[4],
            'item_name' :      item[-1]
        }
        name_list = item[-1].split('.', 2)
        parsed_name = ''.join((name_list[0:2]))
        file_type = name_list[-1]
        bad_words = ('chromosome', 'abinitio')
        data_types = ('dna.toplevel.fa.gz', 'gff3.gz')
        if any( bw in parsed_name for bw in bad_words):
            return
        elif file_type.endswith('dna.toplevel.fa.gz'):
            self.add_genome(parsed_name,
                       fasta_size=line_dict['size'],
                       fasta_uri=''.join((top_dir, item[-1])))
            return
        elif file_type.endswith('gff3.gz'):
            self.add_genome(parsed_name,
                       gff3_size=line_dict['size'],
                       gff3_uri=''.join((top_dir, item[-1])))
            return

    def genome_check(self, item):
        """Checks if the incoming item, which is a single string,
         is a 'genome' (the type of desired data).
         
         :param item: The line of text to be checked.
         
         in that it must:

            + end with fa.gz or gff3.gz
            + not have 'chromosome' in the name
            + must not have 'abinitio' in the name
        
        """
        bad_words = ('chromosome', '.abinitio.')
        data_types = ('dna.toplevel.fa.gz', 'gff3.gz')
        self.logger.debug('GENOME CHECKING: {}'.format(item))
        if item.endswith(data_types) and \
            not any(word in bad_words for word in item):
            return True
        else:
            return False

    def add_genome(self, item,  # TODO: Rename this function? An override?
                   fasta_size=None,
                   gff3_size=None,
                   fasta_uri=None,
                   gff3_uri=None):
        """Creates a new genome. This creates a new isntance of \
        :class:`GenomeEntry`.
        
        :param item: The name of the genome to be created or updated.
        :param fasta_size: The size of the remote fasta, ``.fa.gz`` in bytes.
        :param gff3_size: The size of the remote gff3, ``.gff3.gz`` in bytes.
        :param fasta_uri: The remote uri of the fasta file.
        :param gff3_uri: The remote uri of the gff3 file."""
        genome_entry_args = {
            'fasta_uri'        : fasta_uri,
            'fasta_size'       : fasta_size,
            'gff3_uri'         : gff3_uri,
            'gff3_size'        : gff3_size,
            'download_method'  : 'ftp ensemble'
            }
        # No values set to `None` should pass through.
        g_args = {k : v for k, v in genome_entry_args.items() if v}
        self.save_genome(item, **g_args)

    def dir_check(self, dir_value):
        """Checks if the input: dir_value is a directory. Assumes the input 
        will be in the following format:

             ``"drwxr-sr-x  2 ftp   ftp    4096 Jan 13  2015 filename"``

        This works by checking the first letter of the input string,
        and returns True for a directory or False otherwise."""
        if dir_value[0][0] == 'd':
            return True
        else:
            return False

    def _generate_uri(self):
        """Generates the uri strings needed to download the genomes
        from the ensembl database.

        **Returns**: List of Strings of URIs for the ensembl database. eg::

            'pub/fungi/release-36/gff3/',
            'pub/metazoa/release-36/gff3/',
            ...

        This is an extremely case-sepcific function."""
        ensembl_data_types = ['gff3', 'fasta']
        ensembl_kingdoms = ['fungi', 'metazoa', 'plants', 'protists']
        # Unique permutations of data types and kingdoms.
        uri_gen = itertools.product(ensembl_data_types, ensembl_kingdoms)
        # For each iteration, return the desired URI.
        for item in uri_gen:
            yield '/'.join(('pub', item[1],  # the clade or kingdom
                            self._release_version,
                            item[0], '', ))  # the data type

    def _find_genomes(self,
                      parsing_function,
                      baseURIList):
        """Private function that handles finding the list of genomes.
        
        :param parsing_function: This should be a function that reads an
            ``ftplib.dir()`` line output. This output should always be a
            file, not a directory.
        :param baseURIList: This should be a list of base URIs to start
            the ftp crawler from."""
        self.ftp.connect(ensebml_ftp_uri)  # connect to the ensemble ftp
        self.ftp.login()
        for uri in baseURIList:
            logging.info('Parent crawl dir initialized as: {}'.format(uri))
            self.crawl_dir(uri, parsing_function)
        self.ftp.quit()  # close the ftp connection
        return

    def find_genomes(self):
        """OVERWRITES GENOMEDATABASE FUNCTION. Calls the _find_genomes() 
        private function."""
        logging.info("Finding Genomes. This takes approximately 45 minutes...")
        ensemble_base_URIs = [uri for uri in self._generate_uri()]
        self._find_genomes(parsing_function=self.ensemblLineParser,
                           baseURIList=ensemble_base_URIs,)
        return

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

    def get_mutual_genomes(self):
        """Gets the genome entries that have both a fasta and gff3 uri.
        Returns a tuple that contains:

            ``('taxonomic_name', 'fasta_uri', 'fasta_size',\
               'gff3_uri', 'gff3_size')``"""
        # TODO: Investigate a way to complete this query on the sqlite side.
        # TODO: Find a way to return the entire sql entry? Is that what I want?
        s = select([GenomeEntry.taxonomic_name,
                    GenomeEntry.fasta_uri,
                    GenomeEntry.fasta_size,
                    GenomeEntry.gff3_uri,
                    GenomeEntry.gff3_size])
        s_result = self.session.execute(s)  # Run the query.
        # Then get the name (primary key), if all of those entries exist.
        mut_genomes = [tup for tup in s_result if all(tup)]
        return mut_genomes

    def download_genomes(self, download_list, download_location):
        """This function takes an list of genome tuples. These tuples contain:

            ``('taxonomic_name', 'fasta_uri', 'fasta_size',\
               'gff3_uri', 'gff3_size')``
        
        :param download_list: A list of tuples (example shown above) to be
            downloaded.
        :param download_location: The local file location where the files
            will be saved."""
        self.ftp.connect(ensebml_ftp_uri)  # connect to the ensemble ftp
        self.ftp.login()

        for entry in download_list:
            pk, furi, fsize, guri, gsize = entry

            local_fasta_path = os.path.join(download_location, pk + '.fa.gz')
            local_gff3_path = os.path.join(download_location, pk + '.gff3.gz')
            
            # local_fasta_path = ''.join((download_location, pk, '.fa.gz'))
            # local_gff3_path = ''.join((download_location, pk, '.gff3.gz'))

            # if the directory we are saving do does not exist, it will
            # need to be created.
            if not os.path.exists(download_location):
                os.makedirs(download_location)

            self.ftp.retrbinary('RETR {}'.format(furi),
                                open(local_fasta_path, 'w').write)

            self.ftp.retrbinary('RETR {}'.format(guri),
                                open(local_gff3_path, 'w').write)

        self.ftp.quit()  # close the ftp connection
        return
    