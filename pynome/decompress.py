"""
A sript designed to be run through slurm. Requries a database
file locaiton and an index.

Where are my logs?
What environment variables are available?


It should be invoked as part of a slurm batch job:
    python3 pynome/decompress.py <database_path> <idx>
"""

# import os
import sqlite3
import argparse
import sys
# import os
import subprocess
sys.path.append("/data/ficklin/software/pynome/")
from pynome.utils import cd

# TODO: Try something similar to this?
# job_id = os.environ.get('SLURM_JOB_ID')


def unzip(path):
    with cd(path):
        subprocess.run('gunzip *', shell=True)
    return


def main():
    # Create the parser
    parser = argparse.ArgumentParser()
    parser.add_argument('--sql')
    parser.add_argument('--index')
    args = parser.parse_args()
    # Create the sqlite3 connection
    conn = sqlite3.connect(args.sql)
    # Create the sqlite3 pointer
    curs = conn.cursor()
    # Run the query
    curs.execute('SELECT local_path FROM GenomeTable ORDER BY taxonomic_name')
    # Create a list from the query
    genome_list = [xx for xx in curs]
    # Sort the retrieved list
    genome_list.sort()
    # Close the connection to the sql database.
    conn.close()
    # Get the active genome based on the given index:
    # active_genome = genome_list[job_index]
    active_genome = genome_list[int(args.index)]
    unzip(active_genome[0])
    return


if __name__ == "__main__":
    main()
