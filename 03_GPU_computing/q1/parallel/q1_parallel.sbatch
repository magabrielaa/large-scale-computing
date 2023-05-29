#!/bin/bash
#SBATCH --job-name=q1_parallel   # job name
#SBATCH --output=q1_parallel.out # output log file
#SBATCH --time=00:05:00  # 5 minutes of wall time
#SBATCH --nodes=1        # 1 GPU node
#SBATCH --partition=gpu2 # GPU2 partition
#SBATCH --ntasks=1       # 1 CPU core to drive GPU
#SBATCH --gres=gpu:1     # Request 1 GPU
#SBATCH --account=macs30113

module load cuda/11.0
module load python/anaconda-2019.03

python3 q1_parallel.py