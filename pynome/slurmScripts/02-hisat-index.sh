#!/bin/bash

#SBATCH --partition=ficklin
#SBATCH --account=ficklin

#SBATCH --nodes=1              ### Node count required for the job
#SBATCH --ntasks=1             ### Number of sruns for each job array index

#SBATCH --time=0-01:00:00      ### Wall clock time limit in Days-HH:MM:SS

#SBATCH --job-name=decompress-%A_%a
#SBATCH --output=/scidas/logs/decompress.log
#SBATCH --error=/scidas/logs/decompress-ERRORS.log
#SBATCH --open-mode=append     ### Set the log to append 

#SBATCH --array=0-56

module load python3
module load hisat2

for i in {1..20}; do
	INDEX=$(($SLURM_ARRAY_TASK_ID * 20 + $i))
	srun --ntasks=1	python3 "/data/ficklin/software/pynome/hisat2_extract_splice_sites.py" \
	--sql=sql=/scidas/genome_test.db --index=$SLURM_ARRAY_TASK_ID
done

# NOTES ON SLURM SCRIPTS
# %A will be replaced by the value of SLURM_ARRAY_JOB_ID
# %a will be replaced by the value of SLURM_ARRAY_TASK_ID

