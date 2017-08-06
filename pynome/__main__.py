"""Retrieves genome data files & metadata form online databases.

In this version (0.1.0) only the Ensembl database is implemented.

Usage:
    pynome [--mode=find-genomes]
    pynome [--mode=download-genomes] [--download-dir=DIRECTORY]
"""
import logging
import argparse
from pynome.genomedatabase import GenomeEntry, GenomeDatabase, Base
from pynome.ensembldatabase import EnsemblDatabase
from sqlalchemy import MetaData, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

metadata = MetaData()

logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

    


def entry_find_genomes(database_path='sqlite:///pynome.db'):
    # get the number of genomes.
    # TODO: check if the database exists
    # build the database_path
    # Base = declarative_base()
    engine = create_engine(database_path)
    # Base.metadata.create_all(engine)
    # Create all the tables defined above.
    # create the database instance
    db = EnsemblDatabase(engine)
    Base.metadata.create_all(engine)
    print('#'*80)
    print('This will take some time. Finding genomes...')
    db.find_genomes()
    # query the length returned by get_mutual_genomes()
    mut_genomes = db.get_mutual_genomes()
    print('Found {} genomes to download.'.format(len(mut_genomes)))
    total_size = sum(mut_genomes[:][-2])
    print('There is a total size of {} bytes.'.format(total_size))

def entry_download_genomes():
    pass

def main():

    print('Pynome Main called.')

    FunctionMap = {
        'find-genomes' : entry_find_genomes,
        'download-genomes': entry_download_genomes,
    }

    parser = argparse.ArgumentParser()

    parser.add_argument('-f', '--find-genomes', action='store_true')

    parser.add_argument('-d', '--download-genomes', action='store_true')

    # parser.add_argument('-v', '--verbose',
    #     help='Set output to verbose.',
    #     action='store_true')


    args = parser.parse_args()

    # if args.verbose:
        # logging.basicConfig(level=logging.DEBUG)

    if args.find_genomes:
        print('Finding Genomes!')
        entry_find_genomes()

    if args.download_genomes:
        print('Downloading Genomes!')

    # logging.info('Command line script called')


if __name__ == '__main__':
    main()
