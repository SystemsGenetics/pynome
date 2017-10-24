"""
===================
Tests for ftpHelper
===================

Run from the top dir via::
    ``pytest -sv``

Testing on kamiak:
python3 -m pytest -sv tests/test_ensemblDB.py

Testing on workstation:
python3 -m pytest -sv tests/test_ensemblDB.py

Testing on workstation with command line arguments.
python3 -m pytest -sv tests/test_ensemblDB.py /media/tylerbiggs/genomic/test.db /media/tylerbiggs/genomic/test_genomes/

Testing on KAMIAK with command line arguments.
python3 -m pytest -sv tests/test_ensemblDB.py /scidas/genome_test.db /scidas/test_genomes/
python3 -m pytest -sv tests/test_ensemblDB.py --database=/scidas/genome_test.db --genome=/scidas/test_genomes/
pytest -sv tests/test_ensemblDB.py --database=/scidas/genome_test.db --genome=/scidas/test_genomes/

idev --account=ficklin --partition=ficklin --time=48:00:00
"""

# import pytest
import logging
# from pynome.ensembl import EnsemblDatabase

logging.getLogger(__name__)
logging.basicConfig(
    filename='database_test.log',
    filemode='w',
    level='DEBUG'
)


def test_generate_uri(create_database):
    uri_list = create_database.generate_uri()
    for uri in uri_list:
        logging.info(uri)


crawl_test_uri = [
    'pub/fungi/release-36/gff3/fungi_rozellomycota1_collection/',
    'pub/fungi/release-36/fasta/fungi_rozellomycota1_collection/',
    'pub/fungi/release-36/gff3/fungi_ascomycota1_collection/_candida_glabrata/',
    'pub/fungi/release-36/fasta/fungi_ascomycota1_collection/_candida_glabrata/',
    # 'pub/fungi/release-36/gff3/fungi_ascomycota1_collection/',
    # 'pub/fungi/release-36/fasta/fungi_ascomycota1_collection/'
]


def test_ensemble_crawl(create_database):
    create_database.find_genomes(crawl_test_uri)
    genomes = create_database.get_found_genomes()
    for q in genomes:
        logging.info(str(q))


def test_estimate_download_size(create_database):
    size_estimate = create_database.estimate_download_size()
    logging.info('Size estimate: {}'.format(size_estimate))


def test_generate_metadata_uri(create_database):
    uri_list = create_database.generate_metadata_uri()
    logging.info("Printing metadata information.")
    for uri in uri_list.items():
        logging.info(uri)


def test_download_metadata(create_database):
    logging.info("Downloading metadata.")
    create_database.download_metadata()


def test_download_genomes(create_database):
    create_database.download_genomes()


def test_read_species_metadata(create_database):
    create_database.read_species_metadata()


def test_add_taxonomy_ids(create_database):
    create_database.add_taxonomy_ids()


def test_decompress_genomes(create_database):
    create_database.decompress_genomes()


def test_generate_hisat_index(create_database):
    create_database.generate_hisat_index()


def test_generate_splice_sites(create_database):
    create_database.generate_splice_sites()


def test_generate_gtf(create_database):
    create_database.generate_gtf()
