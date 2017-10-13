"""
A sript designed to be run through slurm. Requries a database
file locaiton and an index.

It should be invoked as part of a slurm batch job:
    python3 pynome/slurmSpliceSite.py <database_path> <idx>
"""

import argparse
import sys
# Some path hackery needed while pynome isn't fully completed.
sys.path.append("/data/ficklin/software/pynome/")
from pynome.utils import cd, slurm_index_interpreter
from pynome.hisat2_extract_splice_sites import extract_splice_sites


def generate_splice_sites(path, gft_infile, outfile="Splice_sites.txt"):

    with cd(path):
        extract_splice_sites(gft_infile, outfile)
    return


def main():
    # Create the parser
    parser = argparse.ArgumentParser()
    parser.add_argument('--sql')
    parser.add_argument('--index')
    args = parser.parse_args()

    active_genome = slurm_index_interpreter(
        # Ensure that requests is a (tuple,).
        sql_database=args.sql,
        index=int(args.index),
        requests=("local_path", "base_filename"),
    )

    generate_splice_sites(
        path=active_genome[0],
        gft_infile=active_genome[1] + ".gft",
    )

    return


if __name__ == "__main__":
    main()
