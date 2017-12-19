# -*- coding: utf-8 -*-

"""
======================
Command Line Interface
======================
"""

# Basic Python package imports.
import os
import sys
import json
import errno
import click
import collections
from tqdm import tqdm

# Intra-package imports.
from pynome.sra import (
    build_sra_query_string,
    run_sra_query,
    fetch_sra_info,
    parse_sra_query_response,
    get_SRA_accession,
    build_sra_path)
from pynome.EnsemblDatabase import EnsemblDatabase
from pynome.SQLiteStorage import SQLiteStorage

# Error handling imports.
from sqlalchemy.exc import SQLAlchemyError, DBAPIError


@click.group()
def entry_point():
    """
    This is the function which the command line invocation
    of pynome calls, right now this does nothing but serve as
    a prefix to other pynome-specific commands.
    """
    pass


@entry_point.group()
def sra():
    """
    The group handler for SRA subscripts.
    """
    pass


@entry_point.command()
@click.option('--sql_path')
@click.option('--genome_path')
def new_db(sql_path, genome_path):
    """
    Create a new sqlite db with the table defined in
    `SQLiteStorage.py`.

    :returns:
        Prints the status of the creation to the terminal.
    """
    click.echo('\nCreating a new SQLite database at: {}'
               .format(sql_path))

    # Create the file and any intermediate directories, raise
    # an error if a file exists at the supplied sql_path.
    try:
        os.makedirs(os.path.dirname(sql_path))
    except OSError as e:
        # Check if the directory / file already exists.
        if e.errno == errno.EEXIST:
            click.echo('Directory already exists...\nExiting...')
            sys.exit()
        else:
            # Raise the last exception in the current scope.
            raise
            sys.exit()

    # Now that the database file has been created, initialize it
    # as a database specifically for Genome Assemblies.
    try:
        # Initiliaze the SQLite table. This creates an empty SQL
        # table with column names for a Genome Assembly.
        storage = SQLiteStorage(database_path=sql_path)
        main_database = EnsemblDatabase(
            database_path=sql_path,
            download_path=genome_path,
            Storage=storage)
    except (SQLAlchemyError, DBAPIError) as e:
        click.echo("Unable to create a new SQL database.\n")
        raise
        sys.exit()

    # Display the status of the requested operation.
    click.echo('Database created. Displaying information...\n')
    click.echo(main_database)


@entry_point.command()
@click.option('--sql_path')
@click.option('--genome_path')
@click.option('--source', default='ensembl')
def update_database(sql_path, genome_path, source='ensembl'):
    """
    Update the sqldatabase provided in `database_path` with
    data pulled from `source`.

    This currently defaults to, and only supports, the
    `source='ensembl' remote source.

    :returns:
        A progress bar of the update progress, and a summary
        of the output.
    """
    # Initialize the connection to the supplied database.
    click.echo('Connecting to database...')
    try:
        # Create the SQLiteStorage instance.
        storage = SQLiteStorage(database_path=sql_path)
        # Create the database instance.
        main_database = EnsemblDatabase(
            database_path=sql_path,
            download_path=genome_path,
            Storage=storage)
    except (SQLAlchemyError, DBAPIError) as e:
        click.echo("Unable to connect to the SQL database.\n")
        raise
        sys.exit()

    click.echo('Connection established...')
    uri_list = main_database.generate_uri()
    click.echo('URI list generated, finding genomes...\n')
    main_database.find_genomes(uri_list=uri_list)
    # TODO: Download the species.txt file and parse it.


@entry_point.command()
@click.option('--sql_path')
@click.option('--genome_path')
# @click.option('--db_col_source')
def download_remote_files(sql_path, genome_path):
    """
    Downloads the remote file from the url stored in the
    sqlite column labeled `db_col_source`. It stores the
    remote file according to the ruleset defined in
    `Storate.py`.
    """
    # Initialize the connection to the supplied database.
    click.echo('Connecting to database...')
    try:
        # Create the SQLiteStorage instance.
        storage = SQLiteStorage(database_path=sql_path)
        # Create the database instance.
        main_database = EnsemblDatabase(
            database_path=sql_path,
            download_path=genome_path,
            Storage=storage)
    except (SQLAlchemyError, DBAPIError) as e:
        click.echo("Unable to connect to the SQL database.\n")
        raise
        sys.exit()

    click.echo('Connection established, downloading genomes...\n')
    main_database.download_genomes()
    pass


@entry_point.command()
@click.option('--sql_path')
@click.option('--genome_path')
@click.option('--action', type=click.Choice(
    ['unzip', 'hisat', 'gtf', 'splice']))
def process_genome_file(sql_path, genome_path, action):
    """
    Runs a post-process on a downloaded file.

    :param database_path:
        The database from which local file paths will
        be read.

    :param action:
        The process to run on the genome file. Available
        options include: `['unzip', 'hisat', 'gtf', 'splice']`
    """
    click.echo('Connecting to database...')
    try:
        # Create the SQLiteStorage instance.
        storage = SQLiteStorage(database_path=sql_path)
        # Create the database instance.
        main_database = EnsemblDatabase(
            database_path=sql_path,
            download_path=genome_path,
            Storage=storage)
    except (SQLAlchemyError, DBAPIError) as e:
        click.echo("Unable to connect to the SQL database.\n")
        raise
        sys.exit()

    click.echo('Connection established...\n')
    # Define a dictioary that maps action arguments to their functions.
    action_dict = {
        'unzip': main_database.decompress_genomes,
        'hisat': main_database.generate_hisat_index,
        'gtf': main_database.generate_gtf,
        'splice': main_database.generate_splice_sites,
    }

    # Run the requested function.
    click.echo('Running the requested action: {0}'.format(action))
    action_dict[action]()
    click.echo('\nAction complete.')


#     if args.read_metadata:
#         try:
#             main_database.read_species_metadata()
#             main_database.add_taxonomy_ids()
#         except:
#             print('Unable to read the metadata file: species.txt')
#
#     if args.uncompress:
#         main_database.decompress_genomes()
#
#     if args.hisat_index:
#         main_database.generate_hisat_index()
#
#     if args.gen_gtf:
#         main_database.generate_gtf()
#
#     if args.gen_splice:
#         main_database.generate_splice_sites()


# @click.command()
# @click.option(
#     '--tax_ID_list',
#     help=('The taxonomy ID on which to base the search.'))
# @click.option(
#     '--path',
#     help='The base path to download SRA .json files.')
# def download_sra_json_by_taxID(tax_id_list, path):
#     """
#     Runs a query for accession numbers based on an given
#     taxonomy identification number.

#     This is a modified functino from the `sra` module with
#     added progress bars for CLI usage.

#     :param tax_id_list:
#         The taxonomy ID that forms the basis of the query
#         for the returned accession numnbers.

#     :param path:
#         The path to download the SRA .json files.

#     :returns:
#         Prints to the terminal a list of matching accession
#         numbers.
#     """
#     # Create the output status dictionary to track whether a given
#     # taxonomy ID was downloaded successfully or not.
#     click.echo('Function called.')
#     status_dict = collections.defaultdict()

#     # For each of the taxonomy ID numbers provided.
#     for tid in tqdm(tax_id_list):

#         # Generate the corresponding query.
#         query = build_sra_query_string(tid)

#         # Run the query.
#         query_response = run_sra_query(query)

#         # Parse the response, get the list of SRA identification
#         # numbers so that the corresponding metadata can be
#         # downloaded.
#         fetch_id_list = parse_sra_query_response(query_response)

#         # If there are any accession values found.
#         if fetch_id_list is not None:

#             # Iterate through the fetch ID numbers.
#             for fetch_id in tqdm(fetch_id_list):

#                 # Get the desired *.json file associated with
#                 # the current fetch ID.
#                 fetch_result = fetch_sra_info(fetch_id)

#                 # Get the ERR or SRR from the fetched result. This
#                 # can be a list of values.
#                 SRA_accession_list = get_SRA_accession(fetch_result)

#                 for sra_id in tqdm(SRA_accession_list):
#                     # print('sra_id', sra_id)

#                     # Create the broken up path.
#                     path = build_sra_path(sra_id)
#                     # print(path)

#                     # Write the accession number to the output dictionary.
#                     status_dict[tid].extend(sra_id)

#                     # Create this path if it does not exist.
#                     if not os.path.exists(path):
#                         os.makedirs(path)

#                     # Write the file.
#                     with open(
#                         os.path.join(
#                             path, sra_id + '.sra.json'), 'w') as nfp:
#                         nfp.write(json.dumps(fetch_result))

#     click.echo(status_dict)


# import logging
# import argparse
#
#
# logging.getLogger(__name__)
# logging.basicConfig(
#     filename='main.log',
#     filemode='w',
#     level='INFO'
# )
#
#
# def entry_find_genomes(database):
#     """The entry point to find genomes with default options. This should
#     be called from the command line."""
#     # Generate the base uri list:
#     uri_list = database.generate_uri()
#     database.find_genomes(uri_list=uri_list)
#
#
# def entry_download_genomes(database):
#     print("Downloading in progresss!\n")
#     database.download_genomes()
#
#
# def main():
#     """The main command line parser for the Pynome module."""
#     parser = argparse.ArgumentParser()  # Create the parser
#     parser.add_argument('database_path',   # required positional argument
#                         metavar='database-path', nargs=1)
#     parser.add_argument('download_path',   # required positional argument
#                         metavar='download-path', nargs=1)
#     parser.add_argument('-f', '--find-genomes', action='store_true')
#     parser.add_argument('-p', '--print-genomes', action='store_true')
#     parser.add_argument('-d', '--download-genomes', action='store_true')
#     parser.add_argument('-m', '--download-metadata', action='store_true')
#     parser.add_argument('-r', '--read-metadata', action='store_true')
#     parser.add_argument('-u', '--uncompress', action='store_true')
#     parser.add_argument('-i', '--hisat-index', action='store_true')
#     parser.add_argument('-g', '--gen-gtf', action='store_true')
#     parser.add_argument('-s', '--gen-splice', action='store_true')
#     parser.add_argument('-v', '--verbose', help='Set output to verbose.',
#                         action='store_true')
#     args = parser.parse_args()  # Parse the arguments
#     logging.info('\nChecking for or creating the database.\n')
#
#     # create the database path if it does not already exist
#     # if not os.path.exists(args.download_path[0]):
#     #     os.makedirs(args.download_path[0])
#
#     try:
#         storage = SQLiteStorage(download_path = args.download_path[0])
#         main_database = EnsemblDatabase(
#           database_path = args.database_path[0],
#           Storage = storage
#         )
#     except:
#         print("Unable to create or read the database!")
#         print('Database Path: {0}'.format(args.database_path[0]))
#         exit()
#
#     if args.verbose:  # Enable verbose logging mode
#         logging.basicConfig(level=logging.DEBUG)
#
#     # check if the database is populated:
#     # if not, and find gemoes is not enabled
#     # exit and print a
#
#     if args.find_genomes:
#         print('Finding Genomes!')
#         entry_find_genomes(main_database)
#
#     if args.print_genomes:
#         print('Printing Genomes!')
#         print(main_database.get_genomes())
#
#     if args.download_metadata:
#         print("Downloading Metadata!")
#         main_database.download_metadata()
#
#     if args.download_genomes:
#         print('Downloading Genomes!')
#         entry_download_genomes(main_database)
#
#     if args.read_metadata:
#         try:
#             main_database.read_species_metadata()
#             main_database.add_taxonomy_ids()
#         except:
#             print('Unable to read the metadata file: species.txt')
#
#     if args.uncompress:
#         main_database.decompress_genomes()
#
#     if args.hisat_index:
#         main_database.generate_hisat_index()
#
#     if args.gen_gtf:
#         main_database.generate_gtf()
#
#     if args.gen_splice:
#         main_database.generate_splice_sites()
#
#     exit()
#
# if __name__ == '__main__':
#     main()
