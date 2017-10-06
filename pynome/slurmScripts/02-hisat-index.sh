#!/bin/bash
#SBATCH --partition=ficklin
#SBATCH --account=ficklin
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --time=8:00:00
#SBATCH --job-name=decompress-%A_%a
#SBATCH --output=~/logs/01-decompress.%a.log
#SBATCH --array=0-1
srun python3 "/data/ficklin/software/pynome/hisat2_extract_splice_sites.py" genomes.db $SLURM_ARRAY_TASK_ID
