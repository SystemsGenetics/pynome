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
from .ensembldatabase import EnsemblDatabase

Metadata = sqlalchemy.MetaData()
Base = sqlalchemy.ext.declarative.declarative_base()

logging.basicConfig()


# def entry_sql_connection():
#     """A wrapper function to handle connecting to the SQL database."""
#     engine = sqlalchemy.create_engine(database_path)
#     database = EnsemblDatabase(engine)
#     Base.metadata.create_all(engine)

def entry_download_metadata(database_path):
    """Entry point for the metadata retrival function. This is a single
    file that is ca. 800 Mb."""
    engine = sqlalchemy.create_engine(database_path)
    database = EnsemblDatabase(engine)
    Base.metadata.create_all(engine)
    metadata_uri = database.generate_metadata_uri()
    database.download_metadata(metadata_uri, 'Genomes')
    return


def entry_find_genomes(database_path):
    """The entry point to find genomes with default options. This should
    be called from the command line."""
    engine = sqlalchemy.create_engine(database_path)
    database = EnsemblDatabase(engine)
    Base.metadata.create_all(engine)
    database.find_genomes()


def entry_download_genomes(database_path):
    """The entry point to download genomes with default options. This should
    be called from the command line."""
    engine = sqlalchemy.create_engine(database_path)
    database = EnsemblDatabase(engine)
    Base.metadata.create_all(engine)
    mutual_genomes = database.get_mutual_genomes()
    genomes_path = os.path.join(database_path, 'Genomes/')
    database.download_genomes(mutual_genomes, genomes_path)


def main():
    """The main command line parser for the Pynome module."""
    parser = argparse.ArgumentParser()  # Create the parser
    parser.add_argument('database_path',   # required positional argument
                        metavar='database-path', nargs=1)
    parser.add_argument('-f', '--find-genomes', action='store_true')
    parser.add_argument('-d', '--download-genomes', action='store_true')
    parser.add_argument('-v', '--verbose', help='Set output to verbose.',
                        action='store_true')
    args = parser.parse_args()  # Parse the arguments

    sqlite_database_dir = 'sqlite:///' + str(args.database_path)

    if args.verbose:  # Enable verbose loggin mode
        logging.basicConfig(level=logging.DEBUG)

    if args.find_genomes:
        print('Finding Genomes!')
        entry_find_genomes(sqlite_database_dir)

    if args.download_genomes:
        print('Downloading Genomes!')
        entry_download_genomes(sqlite_database_dir)


if __name__ == '__main__':
    main()