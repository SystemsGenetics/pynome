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
from pynome.utils import cd, slurm_index_interpreter

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

    active_genome = slurm_index_interpreter(
        requests=("local_path", "base_filename"),
        sql_database=args.sql,
        index=int(args.index)
    )

    unzip(active_genome[0])
    return


if __name__ == "__main__":
    main()
