"""Retrieves genome data files & metadata form online databases.

In this version (0.1.0) only the Ensembl database is implemented.

Usage:
    pynome [--mode=find-genomes]
    pynome [--mode=download-genomes] [--download-dir=DIRECTORY]
"""

import os
import logging
import argparse
from pynome.genomedatabase import GenomeEntry, GenomeDatabase, Base
from pynome.ensembldatabase import EnsemblDatabase
from sqlalchemy import MetaData, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

metadata = MetaData()

logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.DEBUG)

def entry_sql_connection():
    pass

def entry_find_genomes(database_path='sqlite:///pynome.db'):
    # Create an engine for the database
    engine = create_engine(database_path)
    db = EnsemblDatabase(engine)
    Base.metadata.create_all(engine)
    db.find_genomes()

def entry_download_genomes(database_path='sqlite:///pynome.db'):
    engine = create_engine(database_path)
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
    parser.add_argument('-v', '--verbose',help='Set output to verbose.',
                        action='store_true')
    args = parser.parse_args() # Parse the arguments

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
