import unittest
from pynome.ensembldatabase import EnsemblDatabase
from pynome.genome import Genome


class TestEnsemblDatabaseHelperFunctions(unittest.TestCase):

    def test_parse_species_filename(self):

        print("\nInitializing EnsemblDatabase class.")

        # Sample filename taken from the ftp server.
        sample_input = 'Acyrthosiphon_pisum.GCA_000142985.2.36.gff3.gz'
        desired_output = ('Acyrthosiphon_pisum', 'GCA_000142985.2', '36')

        # Generate a new instance of the ensembl database.
        self.test_ensembl_database = EnsemblDatabase()

        # Run the function to test.
        test_case = self.test_ensembl_database._parse_species_filename(sample_input)

        # Assert the desired result.
        self.assertEqual(desired_output, test_case)

    def test_generate_uri(self):

        print("\nInitializing EnsemblDatabase class.")

        # Generate a new instance of the ensembl database.
        self.test_ensembl_database = EnsemblDatabase()

        print("\nGenerating FTP URI for ftp crawling.")
        generated_uri = self.test_ensembl_database._generate_uri()
        for x in generated_uri:
            print('\t', x)

    # TODO: Test function for parse_listings


class TestGenomeInit(unittest.TestCase):

    def test_genome(self):

        # Create an instance of the Genome class.
        self.test_Genome = Genome()

        # Test the assembly version setter
        self.test_Genome.assembly_version = "GCA_000142985.2.36"

        # Test the fasta setter
        self.test_Genome.fasta = "path/to/fa.gz"


if __name__ == '__main__':
    unittest.main()
