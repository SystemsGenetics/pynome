"""
=====================
Slurm Batch Generator
=====================

This script prepares arrays that allow for the access of all downloaded
genomes by pynome. It accomplishes this by connecting to the sqlite database
and creating a list of downloaded genomes. It sorts and counts this list. It
then needs to run one of several jobs.

#. Decompress the genomes.
#. Generate HISAT indexes.
#. Convert the gff3 to a gtf.
#. Generate splice sites.
"""

import sqlite3

SLURM_DECOMPRESS = """#!/bin/bash
#SBATCH --partition=ficklin
#SBATCH --account=ficklin
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --time=8:00:00
#SBATCH --job-name=decompress-%A_%a
#SBATCH --output=logs/01-decompress.%a.log
#SBATCH --array=0-{0}
# Load needed modules
module load python3
# cd into the base genome directory
cd "{1}"
# Get the generated list of genomes
Genome
# SRUN the desired command.
srun python3 "/data/ficklin/software/pynome/slurmScripts/decompress.py" genomes.db $SLURM_ARRAY_TASK_ID

""".format()


def write_slurm_script():
    pass


def submit_slurm_script():
    pass


def order_found_genomes(database_path):
    conn = sqlite3.connect(database_path)
    curs = conn.cursor()
    curs.execute('SELECT * FROM GenomeTable ORDER BY taxonomic_name')
    genome_list = [xx for xx in curs]
    genome_list.sort()
    conn.close()
    return genome_list
