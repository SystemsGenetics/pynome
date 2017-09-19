"""
A sript designed to be run through slurm. Requries a database
file locaiton and an index.

It should be invoked:
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
    # Create the required, positional argumetnssqsl.
    parser.add_argument('database', nargs=1)
    parser.add_argument('', nargs=1)
    # Parse the arguments
    args = parser.parse_args()
    # Create the sqlite3 connection
    conn = sqlite3.connect(args.database)
    # Create the sqlite3 pointer
    curs = conn.cursor()
    # Run the query
    curs.execute('SELECT * FROM GenomeTable ORDER BY taxonomic_name')
    # Create a list from the query
    genome_list = [xx for xx in curs]
    # Sort the retrieved list
    genome_list.sort()
    # Create the path
    conn.close()
    genome_path = genome_list.args.index.taxonomic_name
    unzip(genome_path)
    return


if __name__ == "__main__":
    main()
