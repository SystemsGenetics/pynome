#!/bin/bash
#SBATCH --partition=ficklin
#SBATCH --account=ficklin
#SBATCH --nodes=1              ### Node count required for the job
#SBATCH --ntasks-per-node=1    ### Nuber of tasks to be launched per Node
#SBATCH --time=0-01:00:00      ### Wall clock time limit in Days-HH:MM:SS
#SBATCH --job-name=decompress-%A_%a
#SBATCH --output=logs/01-decompress.%a.log
#SBATCH --array=0-1
python "/data/ficklin/software/pynome/slurmScripts/decompress.py" /scidas/genome_test.db $SLURM_ARRAY_TASK_ID
# NOTES ON SLURM SCRIPTS
# %A will be replaced by the value of SLURM_ARRAY_JOB_ID
# %a will be replaced by the value of SLURM_ARRAY_TASK_ID