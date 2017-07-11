import itertools
import ftplib
from .genomedatabase import GenomeDatabase  # import superclass


class EnsemblDatabase(GenomeDatabase):

    def __init__(self, release_version="release-36"):
        super(GenomeDatabase, self).__init__()
        self._release_version = release_version
        self._ftp_genomes = []

    def _crawl_ftp(self, target_directory):
        """
        recursive function to crawl the ftp server to find genome files.
        call _ftp.sendcmd function to get the current URL
        add each file in the current directory to the _ftp_LIST dictionary
        if a new directory is found then recurse _crawlFTP()
        """

        # active_directory_list = []  # create an empty list for the callback
        # ftp.cwd(target_directory)  # change to the target ftp directory
        # ftp.dir(active_directory_list.append)

        pass

    def _generate_uri(self):
        """
        @breif      Generates the uri strings needed to download the genomes
                    from the ensembl database. Dependant on the release
                    version provided.

        @returns    List of Strings of URIs for the ensembl database. eg:

                        "TODO: example uri here"
                        "TODO: format output here"
        """
        __ensembl_data_types = ['gff3', 'fasta']
        __ensembl_kingdoms = ['fungi', 'metazoa', 'plants', 'protists']
        __ensembl_ftp_uri = 'ftp.ensemblgenomes.org'

        # Unique permutations of data types and kingdoms.
        uri_gen = itertools.product(__ensembl_data_types, __ensembl_kingdoms)

        # For each iteration, return the desired URI.
        for item in uri_gen:
            yield '/'.join((__ensembl_ftp_uri,
                            'pub',
                            item[1],
                            self._release_version,
                            item[0],
                            '',
                            ))

    def _parse_listings(self, dir_list):
        # TODO: Refactor this function into two functions. (parse, interpret)
        """
                @breif      Parses the list of files from the ftplib.FTP.dir()
                            command. Output from this command comes in the form:

                                'drwxr-sr-x    2 ftp   ftp    4096 Jan 13  2015 EB'

                @returns    a list? or a tuple?
                            isDirectory TRUE or FALSE
                            is fa.gz TRUE or FALSE
                            is gff3.gz TRUE or FALSE
                            has 'chromosome' in the filename TRUE or FALSE
                """

        # Append each split sub-list to a directory list.
        split_dir_list = []  # empty list to hold the sub-lists
        for d in dir_list:
            split_dir_list.append(d.split())

        for d in split_dir_list:
            if d[0][0] == 'd':
                print('{} is a directory.'.format(d[-1]))
                self._crawl_ftp(d[-1])
            elif d[-1].endswith('.gz') and 'chromosome' not in d[-1]:
                # This is then a genome we want to create...
                print('{} identified as a desired file'.format(d[-1]))

        # PSEUDO CODE:
        # split this list of strings by the whitespace
        # check the first entry, the fist value:
        #       'drwxr-sr-x'
        # entry[0][0] in this case would be 'd'
        # if entry[0][0] == 'd':
        #      _crawl_ftp(current_dir, target_directory)
        # if 'chromosome' in entry[-1][:]
        #      ignore this chromosome entry
        # if the file ends in ".gff3.gz" or "fa.gz"
        #      then this is a file that should be saved.


        pass

    def _parse_species_filename(self, file_name):
        """<species>.<assembly>.<_version>.gff3.gz"""
        p = file_name.split('.')
        species = p[0]
        assembly = p[1] + '.' + p[2]
        version = p[-3]

        return (species, assembly, version)

    def find_genomes(self):
        """        OVERWRITES GENOMEDATABASE FUNCTION."""
        with ftplib.FTP('ftp.ensemblgenomes.org') as ftp:
            ftp.login()  # login to the ftp server anonymously
            # for item in _generate_url
            # self._crawl_ftp(item)

    @property
    def release_version(self):
        """Release version property. Should be in the form:
            "release-#", "release-36"
        """
        return self._release_version

    def download_genomes(self):
        """Downloads the genomes in the database that have both fasta and gff3 files."""
        pass
