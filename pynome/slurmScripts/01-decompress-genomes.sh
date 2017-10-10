#!/bin/bash

#SBATCH --partition=ficklin
#SBATCH --account=ficklin

#SBATCH --nodes=1              ### Node count required for the job
#SBATCH --ntasks=1             ### Number of sruns for each job array index

#SBATCH --time=0-01:00:00      ### Wall clock time limit in Days-HH:MM:SS

#SBATCH --job-name=decompress-%A_%a
#SBATCH --output=/scidas/logs/01-decompress.log
#SBATCH --error=/scidas/logs/01-decompress-ERRORS.log

#SBATCH --array=0-56

for i in {1..20}; do
	INDEX=$(($SLURM_ARRAY_TASK_ID * 20 + $i))
	srun --ntasks=1	python3 /data/ficklin/software/pynome/pynome/decompress.py \
	--sql=/scidas/genome_test.db --index=$INDEX 
done

# NOTES ON SLURM SCRIPTS
# %A will be replaced by the value of SLURM_ARRAY_JOB_ID
# %a will be replaced by the value of SLURM_ARRAY_TASK_ID