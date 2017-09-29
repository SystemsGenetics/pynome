#!/bin/bash
#SBATCH --partition=ficklin
#SBATCH --account=ficklin
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --time=8:00:00
#SBATCH --job-name=decompress-%A_%a
#SBATCH --output=logs/01-decompress.%a.log
#SBATCH --array=0-1
module load python3
cd "/scidas/genomes3"
# Get all the directories
srun python3 "/data/ficklin/software/pynome/slurmScripts/decompress.py" /scidas/genomes.db $SLURM_ARRAY_TASK_ID
# NOTES ON SLURM SCRIPTS
# %A will be replaced by the value of SLURM_ARRAY_JOB_ID
# %a will be replaced by the value of SLURM_ARRAY_TASK_ID