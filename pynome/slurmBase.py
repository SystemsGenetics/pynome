
SLURM_TEST = """\
#!/bin/bash
#SBATCH --partition=ficklin
#SBATCH --job-name=test
#SBATCH --output=res.txt
#
#SBATCH --ntasks=1
#SBATCH --time=10:00
#SBATCH --mem-per-cpu=100

srun hostname
srun sleep 60
"""

SLURM_DECOMPRESS = """\
#!/bin/bash
#SBATCH --partition=ficklin                 ### Partition
#SBATCH --job-name=decompressGenomesArray   ### Job Name
#SBATCH --nodes=5 							### Number of nodes
#SBATCH --ntasks=1							### Tasks per array job
#SBATCH --array=0-

echo "I am Slurm job ${SLURM_JOB_ID}, array job ${SLURM_ARRAY_JOB_ID}, and array task ${SLURM_ARRAY_TASK_ID}."

python3 -m pynome 

"""
