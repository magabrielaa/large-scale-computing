#!/bin/bash

#SBATCH --job-name=q3_serial
#SBATCH --output=q3_serial.out
#SBATCH --ntasks=1
#SBATCH --partition=broadwl
#SBATCH --constraint=fdr
#SBATCH --account=macs30113
#SBATCH --mem=25G        # total memory per node

# Load Python and MPI module
module load python/anaconda-2019.03

# Run the python program
python3 q3_serial.py