#!/bin/bash
#SBATCH --no-requeue
#SBATCH --job-name="osurun"
#SBATCH --get-user-env
#SBATCH --account=                 #<-- specify the account
#SBATCH --partition=               #<-- specify the partition
#SBATCH --nodes=2
#SBATCH --ntasks-per-node=1
#SBATCH --ntasks=2
#SBATCH --cpus-per-task=24
#SBATCH --mem=100GB
#SBATCH --time=01:30:00
#SBATCH --exclusive           # no other jobs on the node to avoid interference

####
# vars
####
mpimodule=openMPI/4.1.5/gnu/12.2.1
bindir=$(pwd)/../../osu-bin
benchdir=$bindir/libexec/osu-micro-benchmarks/mpi/pt2pt
fileprefix=baremetal-2-nodes

niter=30

# to use ethernet instead of infiniband
mpiflags="--map-by node -x UCX_NET_DEVICES=bond0 -x UCX_MAX_EAGER_RAILS=1 -x UCX_MAX_RNDV_RAILS=1"
export OMPI_MCA_btl="^ofi,usnic,openib"
export OMPI_MCA_mtl="^ofi"



####
# Standard preamble for debugging
####
echo "---------------------------------------------"
echo "SLURM job ID:        $SLURM_JOB_ID"
echo "SLURM job node list: $SLURM_JOB_NODELIST"
echo "DATE:                $(date)"
echo "---------------------------------------------"
module load $mpimodule


####
# Actual benchmark
####


###  Latency  ####

benchmark=$benchdir/osu_latency
filename=$fileprefix-latency.txt
resultfile=$(pwd)/../../out/$filename


echo "Running OSU MPI benchmark"
echo "  binary: $benchmark"
echo "  result file: $resultfile"

for i in $(seq 1 $niter); do
  echo "  iteration $i"
  mpirun -np 2 $mpiflags $benchmark | tee -a $resultfile
done
echo "==================================="


benchmark=$benchdir/osu_latency_mp
filename=$fileprefix-latency_mp.txt
resultfile=$(pwd)/../../out/$filename


echo "Running OSU MPI benchmark"
echo "  binary: $benchmark"
echo "  result file: $resultfile"

for i in $(seq 1 $niter); do
  echo "  iteration $i"
  mpirun -np 2 $mpiflags $benchmark | tee -a $resultfile
done
echo "==================================="

benchmark=$benchdir/osu_multi_lat
filename=$fileprefix-multi-latency.txt
resultfile=$(pwd)/../../out/$filename


echo "Running OSU MPI benchmark"
echo "  binary: $benchmark"
echo "  result file: $resultfile"

for i in $(seq 1 $niter); do
  echo "  iteration $i"
  mpirun -np 2 $mpiflags $benchmark | tee -a $resultfile
done
echo "==================================="


###  Bandwidth  ###

benchmark=$benchdir/osu_bw
filename=$fileprefix-bw.txt
resultfile=$(pwd)/../../out/$filename


echo "Running OSU MPI benchmark"
echo "  binary: $benchmark"
echo "  result file: $resultfile"

for i in $(seq 1 $niter); do
  echo "  iteration $i"
  mpirun -np 2 $mpiflags $benchmark | tee -a $resultfile
done
echo "==================================="


benchmark=$benchdir/osu_bibw
filename=$fileprefix-bibw.txt
resultfile=$(pwd)/../../out/$filename


echo "Running OSU MPI benchmark"
echo "  binary: $benchmark"
echo "  result file: $resultfile"

for i in $(seq 1 $niter); do
  echo "  iteration $i"
  mpirun -np 2 $mpiflags $benchmark | tee -a $resultfile
done
echo "==================================="


benchmark=$benchdir/osu_mbw_mr
filename=$fileprefix-mbw_mr.txt
resultfile=$(pwd)/../../out/$filename


echo "Running OSU MPI benchmark"
echo "  binary: $benchmark"
echo "  result file: $resultfile"

for i in $(seq 1 $niter); do
  echo "  iteration $i"
  mpirun -np 2 $mpiflags $benchmark | tee -a $resultfile
done
echo "==================================="



echo "---------"
echo "  DONE!"
echo "---------"

