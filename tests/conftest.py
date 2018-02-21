"""This module contains fixtures for pytest.

This file is read by pytest, so fixtures defined here do not need to
be imported in other test modules.

By default fixture functions are run for every test functino which uses them.
If we wish to change this behavior, the `scope` argument can be used. The
options for scope include 'module', 'session', and 'function'.
"""

# General Python imports.
import os

# Import testing package of choice.
import pytest

# Import Pynome-specific classes and functions.
from pynome.utils import read_json_config
from pynome.ensembldatabase import EnsemblDatabase


@pytest.fixture(scope='session')
def test_config():
    """Load the test configuration .json file. This file is loaded from
    "test/test_config.json".
    """

    # Build the path to the test json config file. Assume we are in the
    # project parent directory.
    test_config_path = os.path.join('tests', 'test_config.json')

    return read_json_config(test_config_path)


@pytest.fixture(scope='session')
def test_ed(test_config):
    """Create an instance of EnsemblDatabase for testing.
    """
    ed = EnsemblDatabase(
        name=test_config['ensembl_config']['name'],
        url=test_config['ensembl_config']['url'],
        description=test_config['ensembl_config']['description'],
        ignored_dirs=test_config['ensembl_config']['ignored_dirs'],
        data_types=test_config['ensembl_config']['data_types'],
        ftp_url=test_config['ensembl_config']['ftp_url'],
        kingdoms=test_config['ensembl_config']['kingdoms'],
        release_version=test_config['ensembl_config']['release_version'],
        bad_filenames=test_config['ensembl_config']['bad_filenames'],
        # Optional values.
        crawl_urls=test_config['ensembl_config'].get('crawl_urls')
    )

    return ed
