#!/bin/bash

#SBATCH --partition=ficklin
#SBATCH --account=ficklin

#SBATCH --nodes=1              ### Node count required for the job

#SBATCH --time=0-03:00:00      ### Wall clock time limit in Days-HH:MM:SS

#SBATCH --output=/scidas/genomes_october/gtf_generation.log
#SBATCH --error=/scidas/genomes_october/gtf_generation-ERRORS.log

python3 -m pynome -g /scidas/genomes_october/genome.db /scidas/genomes_october/genomes