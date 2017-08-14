"""
================
Tests for Pynome
================

Testing is handled with pytest.

    $ pytest -s tests/pynome_tests.py

To run tests. The ``-s`` option allows output to be printed to the terminal.
"""

import logging
from pynome.genomedatabase import GenomeTuple 
from pynome.ensembldatabase import EnsemblDatabase
# from .context import pynome


"""
=====================
Tests for GenomeTuple
=====================
"""


def test_genometuple():
    """Test an implemenation of the genometuple"""
    logging.info('Testing initiation of a genometuple...\n')
    test_data = {
        # 'taxonomic_name': 'Pyrenophora_teres',
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
        'sra_ID': 'sra_identifier'
    }
    test_genome = GenomeTuple('Pyrenophora_teres', **test_data)
    print(test_genome)


"""
=========================
Tests for EnsemblDatabase
=========================
"""





def test_generate_metadata_uri(database):
    """Run the metadata generator"""
    logging.info(database.generate_metadata_uri())
    assert database.generate_metadata_uri() ==\
        '/pub/release-36/species_metadata.json'


# def test_download_metadata():
#     """Test downloading the metadata. This is a ~800 Mb file, so perhaps
#     this test should not always run."""
#     TEDB = EnsemblDatabase(engine)
#     # metadata_uri = TEDB.generate_metadata_uri()


# def test_sqlite_db():
#     print("\nInitializing EnsemblDatabase class.")
#     TEDB = EnsemblDatabase(engine)
#     print('\nSaving sample genome to the database...')
#     # The test genomes taxonomic name:
#     test_name = 'Acyrthosiphon_pisum'
#     # Create some arguments to pass through.
#     arguments = {'genome_fasta_uri'  : 'uri/to/fasta/file.fa.gz',
#                  'fasta_size' : 1234 }
#     arguments2 = {'genome_gff3_uri'   : 'uri/to/gff3/',
#                   'gff3_size' : 4321}
#     arguments3 = {'genome_local_path' : 'local/path/to/TEST/',
#                   'fasta_size' : None}
#     # Test by 'creating' the same genome 3 times, once for each
#     # of the fields to be updated.
#     TEDB.save_genome('Acyrthosiphon_pisum', **arguments)
#     test_query = TEDB.print_genomes()
#     print(test_query)       

#     TEDB.save_genome('Acyrthosiphon_pisum', **arguments2)
#     test_query = TEDB.print_genomes()    
#     print(test_query)       

#     TEDB.save_genome('Acyrthosiphon_pisum', **arguments3)
#     test_query = TEDB.print_genomes()
#     print(test_query)

# # def test_crawl_ftp():
# #     crawl_test_uri = ['pub/fungi/release-36/gff3/fungi_rozellomycota1_collection/',
# #     'pub/fungi/release-36/fasta/fungi_rozellomycota1_collection/']
# #     TEDB = EnsemblDatabase(engine)
# #     TEDB._find_genomes(TEDB.ensembl_line_parser, crawl_test_uri)
# #     test_query = TEDB.print_genomes()
# #     logging.info('Printing all Genomes in the test database...\n\n{}'\
# #         .format(test_query))

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
