"""
==================
Tests for ftpHelper
==================

Run from the top dir via::
    ``pytest -sv tests\database_test.py``
"""

import pytest
import logging
from pynome.ensembl import EnsemblDatabase

logging.getLogger(__name__)
logging.basicConfig(
    filename='database_test.log',
    filemode='w',
    level='DEBUG'
)


@pytest.fixture(scope='module')
def create_database(database_path='/media/tylerbiggs/genomic//test.db',
                    download_path='/media/tylerbiggs/genomic/'):
    """Create a database instance. The empty path should create the database
    in memory. Without scope='module', this would be run for every test."""
    logging.info('\nCreating the database.\n')
    database_instance = EnsemblDatabase(
        download_path=download_path,
        database_path=database_path,
    )
    yield database_instance


def test_generate_uri(create_database):
    uri_list = create_database.generate_uri()
    for uri in uri_list:
        logging.info(uri)


crawl_test_uri = [
    'pub/fungi/release-36/gff3/fungi_rozellomycota1_collection/',
    'pub/fungi/release-36/fasta/fungi_rozellomycota1_collection/',
    'pub/fungi/release-36/gff3/fungi_ascomycota1_collection/_candida_glabrata/',
    'pub/fungi/release-36/fasta/fungi_ascomycota1_collection/_candida_glabrata/',
    # 'pub/fungi/release-36/gff3/fungi_ascomycota1_collection/',
    # 'pub/fungi/release-36/fasta/fungi_ascomycota1_collection/'
]
def test_ensemble_crawl(create_database):
    create_database.find_genomes(
        crawl_test_uri
    )
    genomes = create_database.get_found_genomes()
    for q in genomes:
        logging.info(str(q))


def test_estimate_download_size(create_database):
    size_estimate = create_database.estimate_download_size()
    logging.info('Size estimate: {}'.format(size_estimate))


def test_generate_metadata_uri(create_database):
    uri_list = create_database.generate_metadata_uri()
    logging.info("Printing metadata information.")
    for uri in uri_list.items():
        logging.info(uri)


def test_download_metadata(create_database):
    logging.info("Downloading metadata.")
    create_database.download_metadata()


def test_download_genomes(create_database):
    genomes = create_database.get_found_genomes()
    create_database.download_genomes()


def test_read_species_metadata(create_database):
    create_database.read_species_metadata()
    for entry in create_database.species_metadata.itertuples():
        logging.info(entry['taxonomy_id'])
