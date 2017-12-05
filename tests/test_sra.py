"""
==================
SRA Testing Module
==================

"""

import csv
from pynome.sra import (
    build_sra_query_string,
    run_sra_query,
)


# Import the sample list of taxonomy IDs from the test_data file.
with open('test_data/taxonomy_ids.txt', 'r') as sra_id_file:
    sra_list = [id for id in csv.reader(sra_id_file)]


def test_build_sra_query_string():
    """
    Test the generation of an SRA query string.

    This simply runs an assertion on the expected string generated.

    """
    expected_output = (
        'txid3702[Organism:noexp]+AND+biomol+rna[Properties]+AND+'
        'platform+illumina[Properties]+AND+100:1000[ReadLength]+'
        'AND+"paired"[Layout]'
    )

    assert build_sra_query_string('3702') == expected_output


def test_run_sra_query():
    """

    :return:
    """
