#!/bin/bash

# -- Constants

prefix=k8s
niter=30
outdir=$(pwd)/../../out/      # Path of the script: /src/kubernetes
yamldir=$(pwd)/yaml-files/

# -- Checks

if ! [ -x "$(command -v kubectl)" ]; then
    echo 'Error: kubectl is not installed.' >&2
    exit 1
fi

if ! kubectl cluster-info &> /dev/null; then
    echo 'Error: kubectl is not connected to the cluster.' >&2
    exit 1
fi

if [ ! -d $outdir ]; then
    mkdir -p $outdir
fi

if [ ! -d $yamldir ]; then
    echo "Error: $yamldir does not exist."
    exit 1
fi


echo "----------- Running the run_all_benchmarks.sh script ---------------"

########
##  2 nodes
########

# -- Latency

bench=$yamldir/2-nodes-latency.yaml
fileout=$outdir/$prefix-2-nodes-latency.txt
./run_benchmark.sh $bench $fileout $niter

bench=$yamldir/2-nodes-latency_mp.yaml
fileout=$outdir/$prefix-2-nodes-latency_mp.txt
./run_benchmark.sh $bench $fileout $niter

bench=$yamldir/2-nodes-multi-latency.yaml
fileout=$outdir/$prefix-2-nodes-multi-latency.txt
./run_benchmark.sh $bench $fileout $niter

# -- Bandwidth

bench=$yamldir/2-nodes-bw.yaml
fileout=$outdir/$prefix-2-nodes-bw.txt
./run_benchmark.sh $bench $fileout $niter

bench=$yamldir/2-nodes-bibw.yaml
fileout=$outdir/$prefix-2-nodes-bibw.txt
./run_benchmark.sh $bench $fileout $niter

bench=$yamldir/2-nodes-mbw_mr.yaml
fileout=$outdir/$prefix-2-nodes-mbw_mr.txt
./run_benchmark.sh $bench $fileout $niter

echo "----------- end of run_all_benchmarks.sh script ---------------"
