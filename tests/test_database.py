"""
==================
Tests for database
==================

Run from the top dir via::
    ``pytest -sv tests\database_test.py``
"""

import pytest
import logging
from pynome.database import GenomeDatabase

logging.getLogger(__name__)
logging.basicConfig(
    filename='database_test.log',
    filemode='w',
    level='DEBUG'
)


@pytest.fixture(scope='module')
def create_database(database_path=':memory:', download_path='tmp'):
    """Create a database instance. The empty path should create the database
    in memory. Without scope='module', this would be run for every test."""
    logging.info('\nCreating the database.\n')
    database_instance = GenomeDatabase(
        database_path=':memory:',
        download_path='tmp')
    yield database_instance


def test_save_genome(create_database):
    """Test saving databases."""
    arguments1 = {
        'taxonomic_name': 'Acyrthosiphon_pisum',
        'fasta_uri': 'uri/to/fasta/file.fa.gz',
        'fasta_size': 1234
    }
    arguments2 = {
        'taxonomic_name': 'Acyrthosiphon_pisum',
        'gff3_uri': 'uri/to/gff3/',
        'gff3_size': 4321
    }
    arguments3 = {
        'taxonomic_name': 'Acyrthosiphon_pisum',
        'local_path': 'local/path/to/TEST/',
        'fasta_size': None
    }

    create_database.save_genome(**arguments1)
    create_database.save_genome(**arguments2)
    create_database.save_genome(**arguments3)


def test_get_all_genomes(create_database):
    """Test printing all genome entries."""
    # create_database.print_genomes()
    genomes = create_database.get_genomes()
    for q in genomes:
        logging.info(str(q))
