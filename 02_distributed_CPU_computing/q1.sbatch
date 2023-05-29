#!/bin/bash

#SBATCH --job-name=q1
#SBATCH --output=q1.out
#SBATCH --ntasks=1
#SBATCH --partition=broadwl
#SBATCH --constraint=fdr
#SBATCH --account=macs30113

# Load Python and MPI modules
module load python/anaconda-2019.03
module load intelmpi/2018.2.199+intel-18.0

# Run the python program with mpirun. The -n flag is not required;
# mpirun will automatically figure out the best configuration from the
# Slurm environment variables.
mpirun python3 ./q1.py