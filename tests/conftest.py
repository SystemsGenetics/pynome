"""
This file is run as part of pytest.
It's use in this application is to load command line options.
"""

import pytest
import logging
from pynome.ensembl import EnsemblDatabase


def pytest_addoption(parser):
    parser.addoption(
        '--database', action='store',
        default='/media/tylerbiggs/genomic/test.db',
        help='Filepath of the sqlite database.')
    parser.addoption(
        '--genome', action='store',
        default='/media/tylerbiggs/genomic/test_genomes/',
        help='Filepath of the sqlite database.')


@pytest.fixture(scope='module')
def database(request):
    return request.config.getoption('--database')


@pytest.fixture(scope='module')
def genome(request):
    return request.config.getoption('--genome')


@pytest.fixture(scope='module')
def create_database(database, genome):
    # database_path='/media/tylerbiggs/genomic/test.db',
    # download_path='/media/tylerbiggs/genomic/test_genomes'):
    """Create a database instance. The empty path should create the database
    in memory. Without scope='module', this would be run for every test."""
    logging.info('\nCreating the database.\n')
    database_instance = EnsemblDatabase(
        download_path=genome,
        database_path=database,
    )
    yield database_instance
