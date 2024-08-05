#!/bin/bash

# Download last version of OSU Micro-Benchmarks

version="7.4"
target="http://mvapich.cse.ohio-state.edu/download/mvapich/osu-micro-benchmarks-$version.tar.gz"
file="osu-micro-benchmarks-$version.tar.gz"

if [ -x "$(command -v curl)" ]; then
    curl -L $target -o $file
elif [ -x "$(command -v wget)" ]; then
    wget $target -O $file
else
    echo "Neither curl nor wget is available. Please install at least one of them."
    exit 1
fi

# Extract the tarball

if [ -x "$(command -v tar)" ]; then
    tar -xf $file
else
    echo "tar command is not available. Please install it."
    exit 1
fi


# create a out directory used to store results and logs and binaries
# dir of this file: /src/slurm
mkdir -p $(pwd)/../../out
mkdir -p $(pwd)/../../osu-bin


# Compile it using the computational node
sbatch compile.sh
