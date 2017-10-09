"""
A sript designed to be run through slurm. Requries a database
file locaiton and an index.

It should be invoked as part of a slurm batch job:
    python3 pynome/slurmGTF.py <database_path> <idx>
"""

import argparse
import sys
import subprocess
# Some path hackery needed while pynome isn't fully completed.
sys.path.append("/data/ficklin/software/pynome/")
from pynome.utils import cd, slurm_index_interpreter


def generate_GTF(path, gff3_infile, gff_outfile):

    cmd = ["gffread", "-T", gff3_infile, "-o", gff_outfile]

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
        # Ensure that requests is a (tuple,).
        sql_database=args.sql,
        index=int(args.index),
        requests=("local_path", "base_filename"),
    )

    generate_GTF(
        path=active_genome[0],
        gff3_infile=active_genome[1] + ".gff3",
        gff_outfile=active_genome[1] + ".gtf",
    )

    return


if __name__ == "__main__":
    main()
