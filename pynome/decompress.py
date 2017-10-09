"""
A sript designed to be run through slurm. Requries a database
file locaiton and an index.

It should be invoked as part of a slurm batch job:
    python3 pynome/decompress.py <database_path> <idx>
"""

import argparse
import sys
import subprocess
# Some path hackery needed while pynome isn't fully completed.
sys.path.append("/data/ficklin/software/pynome/")
from pynome.utils import cd, slurm_index_interpreter


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
        sql_database=args.sql,
        index=int(args.index),
        requests=("local_path",),  # Ensure tuple with a comma
    )

    unzip(active_genome[0])
    return


if __name__ == "__main__":
    main()
