"""
A sript designed to be run through slurm. Requries a database
file locaiton and an index.

It should be invoked as part of a slurm batch job:
    python3 pynome/decompress.py <database_path> <idx>
"""

import sqlite3
import argparse
import subprocess
from pynome.utils import cd


def unzip(path):
    with cd(path):
        subprocess.run('gunzip *', shell=True)
    return


def main():
    # Create the parser
    parser = argparse.ArgumentParser()
    # Create the required, positional arguments
    parser.add_argument('sql', action='store_const')
    parser.add_argument('index', action='store_const')
    # Parse the arguments
    args = parser.parse_args()
    # Create the sqlite3 connection
    conn = sqlite3.connect(args.sql)
    # Create the sqlite3 pointer
    curs = conn.cursor()
    # Run the query
    curs.execute('SELECT * FROM GenomeTable ORDER BY taxonomic_name')
    # Create a list from the query
    genome_list = [xx for xx in curs]
    # Sort the retrieved list
    genome_list.sort()
    # Close the connection to the sql database.
    conn.close()
    # Get the active genome based on the given index:
    active_genome = genome_list[int(args.index)]
    unzip(active_genome.local_path)
    return


if __name__ == "__main__":
    main()
