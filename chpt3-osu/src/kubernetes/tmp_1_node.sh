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
##  1 node
########

# -- Latency

bench=$yamldir/1-node-latency.yaml
fileout=$outdir/$prefix-1-node-latency.txt
./run_benchmark.sh $bench $fileout $niter

bench=$yamldir/1-node-latency_mp.yaml
fileout=$outdir/$prefix-1-node-latency_mp.txt
./run_benchmark.sh $bench $fileout $niter

bench=$yamldir/1-node-multi-latency.yaml
fileout=$outdir/$prefix-1-node-multi-latency.txt
./run_benchmark.sh $bench $fileout $niter

# -- Bandwidth

bench=$yamldir/1-node-bw.yaml
fileout=$outdir/$prefix-1-node-bw.txt
./run_benchmark.sh $bench $fileout $niter

bench=$yamldir/1-node-bibw.yaml
fileout=$outdir/$prefix-1-node-bibw.txt
./run_benchmark.sh $bench $fileout $niter

bench=$yamldir/1-node-mbw_mr.yaml
fileout=$outdir/$prefix-1-node-mbw_mr.txt
./run_benchmark.sh $bench $fileout $niter

echo "----------- end of run_all_benchmarks.sh script ---------------"
