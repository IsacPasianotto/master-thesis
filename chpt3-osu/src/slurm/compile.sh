#!/bin/bash
#SBATCH --no-requeue
#SBATCH --job-name="osucompile"
#SBATCH --get-user-env
#SBATCH --account=                   #<-- your project account 
#SBATCH --partition=                 #<-- your partition
#SBATCH --nodes=1
#SBATCH --cpus-per-task=24
#SBATCH --mem=50GB
#SBATCH --time=00:20:00

mpimodule=openMPI/4.1.5/gnu/12.2.1
osuversion=7.4

# pwd of the script: src/slurm
codedir=$(pwd)/../../osu-micro-benchmarks-$osuversion
outdir=$(pwd)/../../osu-bin

# Standard preamble for debugging
echo "---------------------------------------------"
echo "SLURM job ID:        $SLURM_JOB_ID"
echo "SLURM job node list: $SLURM_JOB_NODELIST"
echo "DATE:                $(date)"
echo "---------------------------------------------"

module load $mpimodule

# Actual job
cd $codedir
./configure CC=mpicc CXX=mpicxx --prefix=$outdir
make
make install

echo "---------"
echo "  DONE!"
echo "---------"
