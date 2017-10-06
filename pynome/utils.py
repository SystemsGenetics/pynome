"""
Utilities for Pynome
"""

import os
import sqlite3


class cd:
    """
    Context manager for changing the current working directory.
    Borrowed from Stackoverflow:
    stackoverflow.com/questions/431684/how-do-i-cd-in-python
    """
    def __init__(self, newPath):
        self.newPath = os.path.expanduser(newPath)

    def __enter__(self):
        self.savedPath = os.getcwd()
        os.chdir(self.newPath)

    def __exit__(self, etype, value, traceback):
        os.chdir(self.savedPath)


def slurm_index_interpreter(
        sql_database,
        index,
        requests=("local_path", "base_filename")):  # a tuple for sqlite3 use
    """
    This script will query a given sql database, then return the
    requested information of the given index position. The entries are
    sorted alphabetical by their taxonomic name.

    :param requests: Must be a tuple of strings that are the desired column
    as defined in `database.py`. By default this tuple is defined to be
    `("local_path", "base_filename")`.

    :param sql_database: The file path of the sqlite database.

    :param index: The integer index of the sqlite database to be operated on.

    :returns: A list of tuples with the requested values (columns) in the
    same order they were requested with.
    """

    # Create the connection and cursor.
    conn = sqlite3.connect(sql_database)
    curs = conn.cursor()

    # Create and run the search, first create the correct number of q marks.
    qmark = "?"
    for item in range(1, len(requests)):
        qmark += ",?"
    # Then construct the search string.
    base_search_str =\
        "SELECT {} FROM GenomeTable ORDER BY taxonomic_name".format(qmark)

    # Now execute the search and pull out the desired genome by its index
    curs.execute(base_search_str, requests)
    genome_list = curs.fetchall()
    desired_genome = genome_list[index]

    # Close the connection
    conn.close()

    return desired_genome
