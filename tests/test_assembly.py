"""Tests for the assembly.py module of Pynome.

"""

from pynome.assembly import Assembly


def test_assembly():
    """Tests for the Assembly class."""

    # Create an assembly.
    no_intra_assembly = Assembly(
        species='testerius',
        genus='genius',
        assembly_id='gtID'
    )

    assert no_intra_assembly.species == 'testerius'
    assert no_intra_assembly.genus == 'genius'
    assert no_intra_assembly.assembly_id == 'gtID'
    assert no_intra_assembly.base_filename == 'genius_testerius-gtID'

    intra_assembly = Assembly(
        species='testerius',
        genus='genius',
        assembly_id='gtID',
        intraspecific_name='intra_Name',
    )

    complete_assembly = Assembly(
        species='testerius',
        genus='genius',
        assembly_id='gtID',
        intraspecific_name='intra_Name',
        version='release-38',
    )
