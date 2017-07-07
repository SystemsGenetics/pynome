from pynome import GenomeDatabase  # import superclass


class EnsemblDatabase(GenomeDatabase):

    def __init__(self, release_version="release-36"):
        self._release_version = release_version
        self._ftp_genomes = []

    def __callback(self):
        """
        Call back function for the _craw_ftp function.
        """
        pass

    def _crawl_ftp(self, current_dir, listing_array):
        """
        recursive function to crawl the ftp server to find genome files.
        call _ftp.sendcmd function to get the current URL
        add each file in the current directory to the _ftp_LIST dictionary
        if a new directory is found then recurse _crawlFTP()
        :param current_dir:
        :param listing_array:
        :return:
        """
        active_directory_list = []  # create an empty list for the callback


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
        pass

    def _parse_listings(self):
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

    def find_genomes(self):
        """
        OVERWRITES GENOMEDATABASE FUNCTION.
        """
        with ftplib.FTP('ftp.ensemblgenomes.org') as ftp:
            ftp.login()  # login to the ftp server anonymously
            # for item in _generate_url
            # self._crawl_ftp(item)

    @property
    def release_version(self):
        """
        @brief      Release version property. Should be in the form:

                        "release-#", "release-36"
        """
        return self._release_version

    def download_genomes(self):
        """
        @brief      Downloads the genomes in the database that have both
                    fasta and gff3 files.

        """
        pass
