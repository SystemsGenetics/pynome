"""Retrieves genome data files & metadata form online databases.

In this version (0.1.0) only the Ensembl database is implemented.

Usage:
    pynome [--mode=find-genomes]
    pynome [--mode=download-genomes] [--download-dir=DIRECTORY]
"""

import os
import logging
import argparse
import sqlalchemy

# from pynome.genomedatabase import GenomeEntry, GenomeDatabase
from pynome.ensembldatabase import EnsemblDatabase

metadata = sqlalchemy.MetaData()
Base = sqlalchemy.ext.declarative.Base()

logging.basicConfig()


def entry_sql_connection():
    pass


def entry_find_genomes(database_path='sqlite:///pynome.db'):
    # Create an engine for the database
    engine = sqlalchemy.create_engine(database_path)
    db = EnsemblDatabase(engine)
    Base.metadata.create_all(engine)
    db.find_genomes()


def entry_download_genomes(database_path='sqlite:///pynome.db'):
    engine = sqlalchemy.create_engine(database_path)
    db = EnsemblDatabase(engine)
    Base.metadata.create_all(engine)

    mutual_genomes = db.get_mutual_genomes()

    curpath = os.path.abspath(os.curdir)
    db.download_genomes(mutual_genomes, os.path.join(curpath, 'Genomes/'))


def main():
    parser = argparse.ArgumentParser()  # Create the parser
    parser.add_argument('-f', '--find-genomes', action='store_true')
    parser.add_argument('-d', '--download-genomes', action='store_true')
    parser.add_argument('-p', '-database-path')
    parser.add_argument('-v', '--verbose', help='Set output to verbose.',
                        action='store_true')
    args = parser.parse_args()  # Parse the arguments

    if args.verbose:  # Enable verbose loggin mode
        logging.basicConfig(level=logging.DEBUG)

    if args.find_genomes:
        print('Finding Genomes!')
        entry_find_genomes()

    if args.download_genomes:
        print('Downloading Genomes!')
        entry_download_genomes()


if __name__ == '__main__':
    main()
