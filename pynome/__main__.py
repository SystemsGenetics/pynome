"""
======================
Command Line Interface
======================

Retrieves genome data files & metadata form online databases.
In this version (0.1.0) only the Ensembl database is implemented.

**SCIDAS**: On SciDAS pynome is located under::

    /data/ficklin/modulefiles/pynome_deploy

**Usage:**::

    python3 -m pynome -h
    usage: __main__.py [-h] [-f] [-p] [-d] [-m] [-r] [-u] [-i] [-g] [-s] [-v]
                       database-path download-path

    positional arguments:
      database-path
      download-path

    optional arguments:
      -h, --help            show this help message and exit
      -f, --find-genomes
      -p, --print-genomes
      -d, --download-genomes
      -m, --download-metadata
      -r, --read-metadata
      -u, --uncompress
      -i, --hisat-index
      -g, --gen-gtf
      -s, --gen-splice
      -v, --verbose         Set output to verbose.


So to run it, and download to a directory on SciDAS storage (from
the pynome dir)::

    # Crawl ensembl and save genomes data to the sqlite database.
    # The download path is still required.
    $ python3 -m pynome -f <sql_db_path> <download_path>

    # Find, download the genomes and metadata file:
    $ python3 -m pynome -fdm <sql_db_path> <download_path>

    # Find, download the genomes and metadata file:
    $ python3 -m pynome -fdm /scidas/genomes2/genome.db /scidas/genomes2
    $ python3 -m pynome -fdm /scidas/genomes/pynome_genome.db /scidas/genomes/enseble_genomes

    # Download the genomes and metadata (genomes must be found)
    $ python3 -m pynome -dm /scidas /scidas/genomes

    # Decompress downloaded genomes
    $ python3 -m pynome -u /scidas/genomes3/ensebl_genome.db /scidas/genomes3

    # Run all post-download processes on downloaded genomes.
    $ python3 -m pynome -uigs /scidas/genomes3/genomes.db /scidas/genomes3

**Testing Examples**::

    $ python3 -m pynome -fdmuigs /media/tylerbiggs/genomic/test.db /media/tylerbiggs/genomic

    srun --partition=ficklin --account=ficklin python3 -m pynome -fdmr /scidas/genomes_october/genome.db /scidas/genomes_october/genomes

    srun --partition=ficklin --account=ficklin python3 -m pynome -uigs /scidas/genomes_october/genome.db /scidas/genomes_october/genomes

    python3 -m pynome -i /scidas/genomes_october/genome.db /scidas/genomes_october/genomes

"""

import logging
import argparse
from pynome.ensembl import EnsemblDatabase
from pynome.SQLiteStorage import SQLiteStorage


logging.getLogger(__name__)
logging.basicConfig(
    filename='main.log',
    filemode='w',
    level='INFO'
)


def entry_find_genomes(database):
    """The entry point to find genomes with default options. This should
    be called from the command line."""
    # Generate the base uri list:
    uri_list = database.generate_uri()
    database.find_genomes(uri_list=uri_list)


def entry_download_genomes(database):
    print("Downloading in progresss!\n")
    database.download_genomes()


def main():
    """The main command line parser for the Pynome module."""
    parser = argparse.ArgumentParser()  # Create the parser
    parser.add_argument('database_path',   # required positional argument
                        metavar='database-path', nargs=1)
    parser.add_argument('download_path',   # required positional argument
                        metavar='download-path', nargs=1)
    parser.add_argument('-f', '--find-genomes', action='store_true')
    parser.add_argument('-p', '--print-genomes', action='store_true')
    parser.add_argument('-d', '--download-genomes', action='store_true')
    parser.add_argument('-m', '--download-metadata', action='store_true')
    parser.add_argument('-r', '--read-metadata', action='store_true')
    parser.add_argument('-u', '--uncompress', action='store_true')
    parser.add_argument('-i', '--hisat-index', action='store_true')
    parser.add_argument('-g', '--gen-gtf', action='store_true')
    parser.add_argument('-s', '--gen-splice', action='store_true')
    parser.add_argument('-v', '--verbose', help='Set output to verbose.',
                        action='store_true')
    args = parser.parse_args()  # Parse the arguments
    logging.info('\nChecking for or creating the database.\n')

    # create the database path if it does not already exist
    # if not os.path.exists(args.download_path[0]):
    #     os.makedirs(args.download_path[0])

    try:
        storage = SQLiteStorage(download_path = args.download_path[0])
        main_database = EnsemblDatabase(
          database_path = args.database_path[0],
          Storage = storage
        )
    except:
        print("Unable to create or read the database!")
        print('Database Path: {0}'.format(args.database_path[0]))
        exit()

    if args.verbose:  # Enable verbose logging mode
        logging.basicConfig(level=logging.DEBUG)

    # check if the database is populated:
    # if not, and find gemoes is not enabled
    # exit and print a

    if args.find_genomes:
        print('Finding Genomes!')
        entry_find_genomes(main_database)

    if args.print_genomes:
        print('Printing Genomes!')
        print(main_database.get_genomes())

    if args.download_metadata:
        print("Downloading Metadata!")
        main_database.download_metadata()

    if args.download_genomes:
        print('Downloading Genomes!')
        entry_download_genomes(main_database)

    if args.read_metadata:
        try:
            main_database.read_species_metadata()
            main_database.add_taxonomy_ids()
        except:
            print('Unable to read the metadata file: species.txt')

    if args.uncompress:
        main_database.decompress_genomes()

    if args.hisat_index:
        main_database.generate_hisat_index()

    if args.gen_gtf:
        main_database.generate_gtf()

    if args.gen_splice:
        main_database.generate_splice_sites()

    exit()

if __name__ == '__main__':
    main()
