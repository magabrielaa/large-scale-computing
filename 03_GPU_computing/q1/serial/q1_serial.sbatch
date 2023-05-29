#!/bin/bash

#SBATCH --job-name=q1_serial
#SBATCH --output=q1_serial.out
#SBATCH --ntasks=1
#SBATCH --partition=broadwl
#SBATCH --constraint=fdr
#SBATCH --account=macs30113

# Load Python and MPI module
module load python/anaconda-2019.03

# Run the python program
python3 q1_serial.py