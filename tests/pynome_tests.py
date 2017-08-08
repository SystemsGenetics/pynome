"""
=========================
Tests for EnsemblDatabase
=========================
"""

import os
from nose.tools import *
import logging
from .context import pynome
from pynome.ensembldatabase import EnsemblDatabase
from sqlalchemy import create_engine, select
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
###############################################################################


## CONFIGURE LOCAL TEST SQLITE SERVER
engine = create_engine('sqlite:///:memory:')
# engine = create_engine('sqlite://///media/tylerbiggs/genomic/PYNOME.db')
pynome.genomedatabase.Base.metadata.create_all(engine)  # Create all the tables defined above.

def setup_EnsemblDB():
    """Set up the ensemblDatabase testing sqlite server in memory."""
    tDatabase = EnsemblDatabase(engine)

def teardown_EnsemblDB():
    pass

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
    TEDB._find_genomes(TEDB.ensembl_line_parser, crawl_test_uri)
    test_query = TEDB.print_genomes()
    logging.info('Printing all Genomes in the test database...\n\n{}'\
        .format(test_query))

def test_download_genomes():
    TEDB = EnsemblDatabase(engine)
    crawl_test_uri = ['pub/fungi/release-36/gff3/fungi_rozellomycota1_collection/',
    'pub/fungi/release-36/fasta/fungi_rozellomycota1_collection/']
    # TEDB._find_genomes(TEDB.ensemblLineParser, crawl_test_uri)

    mg = TEDB.get_mutual_genomes()
    
    logging.info('Printing all genomes with both fasta and gff3 files.\n\n{}'\
        .format(mg))
    curpath = os.path.abspath(os.curdir)
    TEDB.download_genomes(mg, os.path.join(curpath, 'tmp/'))
    

# def test_generate_uri():
#     TEDB = EnsemblDatabase(engine)
#     logging.debug("Generating FTP URI for ftp crawling.")
#     generated_uri = TEDB._generate_uri()
#     for uri in generated_uri:
#         logging.debug('\t{}'.format(uri))