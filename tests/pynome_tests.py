"""
================
Tests for Pynome
================

Testing is handled with pytest.

    $ pytest -s tests/pynome_tests.py

To run tests. The ``-s`` option allows output to be printed to the terminal.
"""

import logging
from .context import pynome

# Set up the logger file
logging.basicConfig(
    filename='tests.log',
    filemode='w',
    level=logging.DEBUG)

# Assign shorter namespaces while maintaing cleaner imports.
GenomeEntry = pynome.genomedatabase.GenomeEntry
Ensebledb = pynome.ensembldatabase.EnsemblDatabase

"""
=====================
Tests for GenomeEntry
=====================
"""


def create_genome_entry():
    """Test an implemenation of the genometuple"""
    test_data = {
        'taxonomic_name': 'Pyrenophora_teres',
        'download_method': 'ensemble_ftp',
        'fasta_uri': ('ftp://ftp.ensemblgenomes.org/pub/fungi/release-36/'
                      'fasta/pyrenophora_teres/dna/Pyrenophora_teres.'
                      'GCA_000166005.1.dna.toplevel.fa.gz'),
        'gff3_uri': ('ftp://ftp.ensemblgenomes.org/pub/fungi/release-36/'
                     'gff3/pyrenophora_teres/Pyrenophora_teres'
                     '.GCA_000166005.1.36.gff3.gz'),
        'local_path': 'local/directory',
        'fasta_remote_size': 123456,
        'gff3_remote_size': 23456789,
        'assembly_name': 'GCA_000166005',
        'genus': 'Pyrenophora',
        'species': 'teres',
        'sra_id': 'sra_identifier',
    }
    test_genome = GenomeEntry(**test_data)
    return test_genome


def test_genome_entry():
    """Test an implemenation of the genometuple"""
    logging.info('Testing initiation of a genometuple...\n')
    test_genome = create_genome_entry()
    logging.info(test_genome)


"""
=========================
Tests for EnsemblDatabase
=========================
"""


def ensembl_init_wrapper(function):
    """Creates an ensembldatabase class instance for testing."""
    ensemble_test_db = Ensebledb()

    def wrapper():
        """The wrapped function to be returned."""
        function(database=ensemble_test_db)
    return wrapper


@ensembl_init_wrapper
def test_generate_metadata_uri(database):
    """Run the metadata generator"""
    logging.info('Generating metadata URI...\n')
    logging.info(database.generate_metadata_uri())
    assert database.generate_metadata_uri() ==\
        '/pub/release-36/species_metadata.json'


@ensembl_init_wrapper
def test_save_genome(database):
    """Create and save a sample geneome to the database."""
    logging.info('Testing saving a genome to the database list...')
    new_genome = create_genome_entry()
    database.save_genome(new_genome)
    return


@ensembl_init_wrapper
def test_print_genome_list(database):
    """Test the console printing of GenomeDatabase."""
    logging.info('Testing the custom __repr__ method for the database...')
    new_genome = create_genome_entry()
    database.save_genome(new_genome)
    logging.info('{}'.format(database.genome_list))
    return


@ensembl_init_wrapper
def test_crawl_ftp(database):
    """Test the ftp crawler with some sample uris"""
    crawl_test_uri = [
        'pub/fungi/release-36/gff3/fungi_rozellomycota1_collection/',
        'pub/fungi/release-36/fasta/fungi_rozellomycota1_collection/'
    ]
    database._find_genomes(database.ensembl_line_parser, crawl_test_uri)
    logging.info('Printing all Genomes in the test database...\n\n{}'
                 .format(database))



# def test_download_metadata():
#     """Test downloading the metadata. This is a ~800 Mb file, so perhaps
#     this test should not always run."""
#     TEDB = EnsemblDatabase(engine)
#     # metadata_uri = TEDB.generate_metadata_uri()



# # def test_download_genomes():
# #     TEDB = EnsemblDatabase(engine)
# #     crawl_test_uri = ['pub/fungi/release-36/gff3/fungi_rozellomycota1_collection/',
# #     'pub/fungi/release-36/fasta/fungi_rozellomycota1_collection/']
# #     # TEDB._find_genomes(TEDB.ensemblLineParser, crawl_test_uri)

#     mg = TEDB.get_mutual_genomes()
#     logging.info('Printing all genomes with both fasta and gff3 files.\n\n{}'\
#         .format(mg))
#     curpath = os.path.abspath(os.curdir)
#     TEDB.download_genomes(mg, os.path.join(curpath, 'tmp/'))
    

# def test_sum_sizes():
#     TEDB = EnsemblDatabase(engine)
#     print(TEDB.estimate_download_size())
