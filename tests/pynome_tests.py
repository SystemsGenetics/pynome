from nose.tools import *
import logging
from pynome.ensembldatabase import EnsemblDatabase
from pynome.genome import Genome


###############################################################################
## NOSETESTS USAGE NOTES
##
## $ nosetests [options] [(optional) test files or directories]
##
## Configuration options can also be placed in:
##      .noserc or nose.cfg
## Where these are standard .ini style config files.
##
## Nosetests in a script:
##      import nose
##      nose.main()
##
## Options:
##      -V, --version
##      -p, --plugins
##      -v=DEFAULT, --verbose=DEFAULT
##      --verbosity=VERBOSITY
##      -l=DEFAULT, --debug=DEFAULT
##      --debug-log=FILE
##      --logging-config=FILE, --log-config=FILE
##      -s. --nocapture 
##          Does not capture print or stdout.
###############################################################################

###############################################################################
## CONFIGURE LOGGER
###############################################################################


# TODO: Download a sampel directory structure from the ensembl ftp site and
#       and save it locally. Use this for the testing, since it takes about
#       45 minutes to work through the genomes on the full site.


def test_ensembl_database():
    # Generate an instance of the ensembl database
    TEDB = EnsemblDatabase()
    # Test that the generated release_version is correct.
    assert_equal(TEDB.release_version, 'release-36')
    
def test_genome_check():
    good_hit = 'Colletotrichum_graminicola.GCA_000149035.1.36.gff3.gz'
    # bad_hits = ('')
    test_ensembl_db = EnsemblDatabase()
    assert_true(test_ensembl_db.genome_check(good_hit))

def test_parse_species_filename():
    # Sample filename taken from the ftp server.
    sample_input = 'Acyrthosiphon_pisum.GCA_000142985.2.36.gff3.gz'
    desired_output = ('Acyrthosiphon_pisum', 'GCA_000142985.2')
    # Generate a new instance of the ensembl database.
    TEDB = EnsemblDatabase() 
    # Run the function to test.
    test_case = TEDB._parse_species_filename(sample_input)
    assert_equal(desired_output, test_case)

def test_generate_uri():
    print("\nInitializing EnsemblDatabase class.")
    # Generate a new instance of the ensembl database.
    TEDB = EnsemblDatabase()
    print("\nGenerating FTP URI for ftp crawling.")
    generated_uri = TEDB._generate_uri()
    for uri in generated_uri:
        print('\t{}'.format(uri))

def test_sqlite_db():
    print("\nInitializing EnsemblDatabase class.")
    TEDB = EnsemblDatabase()
    print('\nSaving sample genome to the database...')
    arguments = {'genome_fasta_uri'  : 'uri/to/fasta/file.fa.gz',
                 'genome_gff3_uri'   : 'uri/to/gff3/',
                 'genome_local_path' : 'local/path/to/files/'}
    TEDB.save_genome('Acyrthosiphon_pisum', **arguments)
    print('\nTesting query/recall from the local database...')
    print('This should display all genomes currently loaded.\n')
    test_query = TEDB.print_genomes()
    print(test_query)
    



# def test_crawl_ftp():
#     test_ensembl_db = EnsemblDatabase()
#     test_ensembl_db.find_genomes()



# def test_genome():

    # Create an instance of the Genome class.
    # test_Genome = Genome()  # default value should be 'release_version=36'

    # value to be tested
    # test_value = test_Genome.release_version()
    # print(test_value)

    # assert_equal('release-36', test_value)
    # Test the assembly version setter
    # test_Genome.assembly_version = "GCA_000142985.2.36"

    # Test the fasta setter
    # test_Genome.fasta = "path/to/fa.gz"
