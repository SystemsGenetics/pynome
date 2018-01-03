"""
==================
Tests for database
==================

Run from the top dir via::
    ``pytest -sv tests\database_test.py``
"""

# import logging

from pynome.genomeassembly import GenomeAssembly

# logging.getLogger(__name__)
# logging.basicConfig(
#     filename='database_test.log',
#     filemode='w',
#     level='DEBUG'
# )


def test_save_genome(create_database):
    """Test saving databases."""
    arguments1 = {
        'genus': 'Rozella',
        'speices': 'allomycis',
        'fasta_uri': (
            'pub/fungi/release-36/fasta/fungi_rozellomycota1_collection/'
            'rozella_allomycis_csf55/dna_index/Rozella_allomycis_csf55.'
            'Rozella_k41_t100.dna.toplevel.fa.gz'),
        'fasta_size': 3700778
    }

    test_assembly_1 = GenomeAssembly(**arguments1)

    arguments2 = {
        'genus': 'Rozella',
        'speices': 'allomycis',
        'gff3_uri': (
            'pub/fungi/release-36/gff3/fungi_rozellomycota1_collection/'
            'rozella_allomycis_csf55/Rozella_allomycis_csf55.'
            'Rozella_k41_t100.36.gff3.gz'),
        'gff3_size': 965829
    }

    test_assembly_2 = GenomeAssembly(**arguments2)

    create_database.save_genome(test_assembly_1)
    create_database.save_genome(test_assembly_2)


def test_get_all_genomes(create_database):
    """Test printing all genome entries."""
    # create_database.print_genomes()
    genomes = create_database.get_genomes()
    for q in genomes:
        logging.info(str(q))
