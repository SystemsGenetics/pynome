"""
This file is run as part of pytest.
It's use in this application is to load command line options.
"""

# General testing imports.
import pytest

# Pynome-specific imports.
from pynome.ensembldatabase import EnsemblDatabase
from pynome.sqlitestorage import SQLiteStorage


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
    """
    Create a database instance. The empty path should create the database
    in memory. Without scope='module', this would be run for every test.
    """
    # Create an instance of the SQLiteStorage class.
    sql_storage = SQLiteStorage(
        download_path=genome,
        database_path=database,
    )

    database_instance = EnsemblDatabase(
        storage=sql_storage
    )
    yield database_instance
