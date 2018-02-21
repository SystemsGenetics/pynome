# """Tests for the ensembldatabse.py module of Pynome.
#
# """
#
# from pynome.ensembldatabase import EnsemblDatabase
#
#
# def test_EnsemblDatabase(test_config):
#
#     # Initialize the EnsemblDatabase
#     ed = EnsemblDatabase(
#         name=test_config['ensembl_config']['name'],
#         url=test_config['ensembl_config']['url'],
#         description=test_config['ensembl_config']['description'],
#         ignored_dirs=test_config['ensembl_config']['ignored_dirs'],
#         data_types=test_config['ensembl_config']['data_types'],
#         ftp_url=test_config['ensembl_config']['ftp_url'],
#         kingdoms=test_config['ensembl_config']['kingdoms'],
#         release_version=test_config['ensembl_config']['release_version'],
#         bad_filenames=test_config['ensembl_config']['release_version'],
#     )
#
#     # Test Ensembl properties.
#     print(f'\nEnsembl metadata URI: {ed.metadata_uri}')
#
#     # Start a crawl on the test directories.
#     # ed.crawl(test_config['ensembl_config']['test_urls'])
#
#     # print([x for x in ed.assemblies])
#
#     ed.download_metadata()
