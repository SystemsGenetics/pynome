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
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

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
## Logging Levels:
##  debug, info, warning, error, critical
##
##
##
##
##
###############################################################################


## CONFIGURE LOCAL TEST SQLITE SERVER
engine = create_engine('sqlite:///:memory:')
# engine = create_engine('sqlite://///media/tylerbiggs/genomic/PYNOME.db')
pynome.genomedatabase.Base.metadata.create_all(engine)  # Create all the tables defined above.

def test_ensembl_database():
    # Generate an instance of the ensembl database
    TEDB = EnsemblDatabase(engine)
    # Test that the generated release_version is correct.
    assert_equal(TEDB.release_version, 'release-36')
    
def test_genome_check():
    good_hit = 'Colletotrichum_graminicola.GCA_000149035.1.36.gff3.gz'
    # bad_hits = ('')
    test_ensembl_db = EnsemblDatabase(engine)
    assert_true(test_ensembl_db.genome_check(good_hit))

def test_generate_uri():
    print("\nInitializing EnsemblDatabase class.")
    # Generate a new instance of the ensembl database.
    TEDB = EnsemblDatabase(engine)
    print("\nGenerating FTP URI for ftp crawling.")
    generated_uri = TEDB._generate_uri()
    for uri in generated_uri:
        print('\t{}'.format(uri))

def test_sqlite_db():
    print("\nInitializing EnsemblDatabase class.")
    TEDB = EnsemblDatabase(engine)
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
    TEDB = EnsemblDatabase(engine)
    TEDB._find_genomes(TEDB.ensemblLineParser, crawl_test_uri)
    test_query = TEDB.print_genomes()
    print(test_query)
    print(TEDB.get_mutual_genomes())

    