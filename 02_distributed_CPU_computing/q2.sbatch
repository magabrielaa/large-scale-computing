#!/bin/bash

#SBATCH --job-name=q2
#SBATCH --output=q2.out
#SBATCH --ntasks=20
#SBATCH --partition=broadwl
#SBATCH --constraint=fdr
#SBATCH --account=macs30113

# Load Python and MPI modules
module load python/anaconda-2019.03
module load intelmpi/2018.2.199+intel-18.0

for i in {1..20}
do
mpirun -n $i python3 q2.py >> q2.out
done