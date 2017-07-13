class GenomeDatabase(object):
    """
    @brief     Base Genome Database class.
               Many functions will have to be overwritten by
               the database-specific child classes.
    """
    def __init__(self):
        """
        @brief     Initialization of the GenomeDatabase class.
        """

        self._baseGenomeDir = None
        self._genomeList = []
        self._downloadProtocol = None

    def save_genomes(self):
        """
        @brief     Save the genomes in this database.
                   Save to the _baseGenomeDir location.
        """
        pass

    def print_genomes(self):
        """
        @brief     Print the Genomes in the database to the terminal.
                   TODO: Implement.
        """
        pass

    def find_genomes(self):
        """
        @brief     To be overwritten by child classes.
                   Very database specific.

        """
        pass

    def download_genomes(self):
        """
        @brief     To be overwritten by child classes.
                   Very database specific.
        """
        pass
