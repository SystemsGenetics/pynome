"""Tests for the assemblystroage.py module of Pynome.

"""
# import logging

from pynome.assemblystorage import AssemblyStorage
from pynome.assembly import Assembly
from pynome.sra import download_sra_json


def test_AssemblyStorage(test_config, test_ed):
    """Test the AssemblyStorage class.

    This is the primary test case for now.
    """

    # Initialize an instance of AssemblyStorage with the test session.
    test_assembly_storage = AssemblyStorage(
        sqlite_path=test_config["storage_config"]["sqlite_path"],
        base_path=test_config["storage_config"]["base_path"])

    # Add the test EnsemblDatabase fixture to the sources list.
    test_assembly_storage.add_source(test_ed)

    # Initiate a crawl through the AssemblyStorage API.
    test_assembly_storage.crawl(
        'ensembl',
        test_config['ensembl_config'].get('crawl_urls'))

    # Download the metadata file.
    test_assembly_storage.sources['ensembl'].download_metadata()

    # Save those assemblies found.
    test_assembly_storage.save_assemblies()

    # Get a list of all asemblies found by the crawl.
    assemblies_from_crawl = test_assembly_storage.query_local_assemblies()

    # Search for matching taxonomy IDs within the species.txt metadata file,
    # and update the assemblies with that information.
    tax_id_update = test_assembly_storage.sources['ensembl'].add_taxonomy_ids(
        assemblies_from_crawl)

    # Save (update) each of these assembly ids.
    for pk, update_dict in tax_id_update:
        test_assembly_storage.update_assembly(pk, update_dict)

    # Assign all found genomes to a list.
    found_genomes = test_assembly_storage.query_local_assemblies()

    # Download the SRA files of the found genomes.
    test_assembly_storage.download_all_sra()

    # Get the taxonomy_IDs from the SQLite database.
    # tax_ids = [gen.taxonomy_id for gen in found_genomes]
    # print(f'Taxonomy IDs: {tax_ids}')

    # Use those taxonomy IDs to fetch the SRA metadata files.
    # download_sra_json(test_assembly_storage.base_sra_path, tax_ids)

    # test_assembly_storage.download(found_genomes)
    test_assembly_storage.download_all()

    # Display all entries.
    print([a for a in found_genomes])

    print('Querty Testing...\n')
    test_query = test_assembly_storage.query_local_assemblies_by(
        'species', 'glabrata'
    )

    print(test_query)

    for a in found_genomes:
        test_assembly_storage.prepare(a)
