"""
Tests for EnsemblDatabase
=========================

## Classes & Assosiated functions

:class GenomeDatabse: 
GenomeEntry
GenomeDatabase
EnsemblDatabase
"""

from nose.tools import *
import logging
from .context import pynome
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
# TODO: Implement a local/fake ftp server for testing? Find a good way to test
#       The recursive function.

# def test_dir_check():
    # TEDB = EnsemblDatabase()


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

# def test_parse_species_filename():
#     # Sample filename taken from the ftp server.
#     sample_input = 'Acyrthosiphon_pisum.GCA_000142985.2.36.gff3.gz'
#     desired_output = ('Acyrthosiphon_pisum', 'GCA_000142985.2')
#     # Generate a new instance of the ensembl database.
#     TEDB = EnsemblDatabase() 
#     # Run the function to test.
#     test_case = TEDB.parse_species_filename(sample_input)
#     assert_equal(desired_output, test_case)

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
    # The test genomes taxonomic name:
    test_name = 'Acyrthosiphon_pisum'
    # Create some arguments to pass through.
    arguments = {'genome_fasta_uri'  : 'uri/to/fasta/file.fa.gz',
                 'fasta_size' : 1234 }
    arguments2 = {'genome_gff3_uri'   : 'uri/to/gff3/',
                  'gff3_size' : 4321}
    arguments3 = {'genome_local_path' : 'local/path/to/TEST/',
                  'fasta_size' : None}
    # Test by 'creating' the same genome 3 times, once for each
    # of the fields to be updated.
    TEDB.save_genome('Acyrthosiphon_pisum', **arguments)
    test_query = TEDB.print_genomes()
    print(test_query)       

    TEDB.save_genome('Acyrthosiphon_pisum', **arguments2)
    test_query = TEDB.print_genomes()    
    print(test_query)       

    TEDB.save_genome('Acyrthosiphon_pisum', **arguments3)
    test_query = TEDB.print_genomes()
    print(test_query)

def test_crawl_ftp():
    crawl_test_uri = ['pub/fungi/release-36/gff3/fungi_rozellomycota1_collection/',
    'pub/fungi/release-36/fasta/fungi_rozellomycota1_collection/']
    TEDB = EnsemblDatabase()
    TEDB._find_genomes(TEDB.ensemblLineParser, crawl_test_uri)
    test_query = TEDB.print_genomes()
    print(test_query)
