"""
==================
SRA Testing Module
==================

"""

import csv
from pynome.sra import (
    build_sra_query_string,
    chunk_accession_id,
)


# Import the sample list of taxonomy IDs from the test_data file.
# with open('test_data/taxonomy_ids.txt', 'r') as sra_id_file:
#     sra_list = [id for id in csv.reader(sra_id_file)]


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


def test_chunk_accession_id():
    """
    Test breaking SRA accession strings into component lists
    for future generation of filepaths.
    """
    assert chunk_accession_id('SRR447617') == ['SRR', '44', '76', '17']
    assert chunk_accession_id('SRR2106895') == ['SRR', '21', '06', '89']
    assert chunk_accession_id('SRR2106895_1') == ['SRR', '21', '06', '89']
