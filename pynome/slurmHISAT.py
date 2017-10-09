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


def gen_hisat_indexes(path, base_name):

    fa_file = base_name + '.fa'
    cmd = ['hisat2-build', '-f', fa_file, base_name]

    with cd(path):
        subprocess.run(cmd)
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
        requests=("local_path", "base_filename"),  # Ensure tuple with a comma
    )

    print(active_genome)
    print(type(active_genome))
    gen_hisat_indexes(
        path=active_genome[0],
        base_name=active_genome[1]
    )
    return


if __name__ == "__main__":
    main()
