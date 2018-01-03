from pynome.genomeassembly import GenomeAssembly


def test_genome_assembly():
    """
    Tests the properties of the GenomeAssembly class.
    """

    # Build the arguments for a sample assembly.
    arg1 = {
        'genus': 'Rozella',
        'species': 'allomycis',
        'assembly_name': 'Rozella_k41_t100',
        'intraspecific_name': 'csf55',
        'fasta_uri': (
            'pub/fungi/release-36/fasta/fungi_rozellomycota1_collection/'
            'rozella_allomycis_csf55/dna_index/Rozella_allomycis_csf55.'
            'Rozella_k41_t100.dna.toplevel.fa.gz'),
        'fasta_size': 3700778
    }

    # Create a GenomeAssembly using the above arguments.
    assembly_1 = GenomeAssembly(**arg1)

    # Test the properties, which should populate themselves.
    assert assembly_1.taxonomic_name == 'Rozella_allomycis_csf55'
    assert assembly_1.base_filename == \
        'Rozella_allomycis_csf55-Rozella_k41_t100'

    # Build the arguments for an assembly without an intraspecific name.
    arg2 = {
        'genus': 'Rozella',
        'species': 'allomycis',
        'assembly_name': 'Rozella_k41_t100',
        'fasta_uri': (
            'pub/fungi/release-36/fasta/fungi_rozellomycota1_collection/'
            'rozella_allomycis_csf55/dna_index/Rozella_allomycis_csf55.'
            'Rozella_k41_t100.dna.toplevel.fa.gz'),
        'fasta_size': 3700778
    }

    assembly_2 = GenomeAssembly(**arg2)

    assert assembly_2.taxonomic_name == 'Rozella_allomycis'
    assert assembly_2.base_filename == \
        'Rozella_allomycis-Rozella_k41_t100'
