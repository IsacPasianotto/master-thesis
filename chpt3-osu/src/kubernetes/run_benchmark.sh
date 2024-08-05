#!/bin/bash

namespace="osu"
targetpodname="launcher"

if [ -z "$(kubectl get namespace $namespace)" ]; then
    echo "The namespace osu does not exist. Please create it first."
    exit 1
fi

if [ $# -lt 3 ]; then
    echo "Wrong number of arguments provided!"
    echo "usage: $0 <yaml_file> <results_file> <number_of_iterations>"
    exit 1
fi

if [ ! -f $1 ]; then
    echo "The file $1 does not exist."
    exit 1
fi

if [ -f $2 ]; then
    read -p "The result file already exists. Do you want to overwrite it? ([N]/y) " overwrite
    if [ "$overwrite" != "y" ]; then
        echo "Exiting..."
        exit 0
    fi
fi

if ! [[ $3 =~ ^[0-9]+$ ]] || [ $3 -le 0 ]; then
    echo "The third argument must be a number greater than 0."
    exit 1
fi

export yaml_file=$1
export results_file=$2
export iterations=$3

for i in $(seq 1 $iterations); do

    printf "\n\nIteration $i/$iterations\n"
    export status=""

    kubectl apply -f $yaml_file --namespace $namespace

    waittime=0
    while [ "$status" != "Completed" ]; do
        status=$(kubectl get pod -n $namespace | grep $targetpodname | awk '{print $3}')
        echo "Waiting for the benchmark to complete..."
        sleep 5
        waittime=$((waittime+5))
        # Sometimes the launcher pod gets stuck. Deleting it and letting the deployment recreate it solves the issue.
        if [ $waittime -ge 180 ]; then
            echo "The benchmark is taking too long. Deleting the launcher pod and waiting for the deployment to recreate it."
            export pod_name=$(kubectl get pods -n $namespace | grep $targetpodname | awk '{print $1}')
            kubectl delete pod $pod_name -n $namespace
            waittime=0
        fi
    done

    export pod_name=$(kubectl get pods -n $namespace | grep $targetpodname | awk '{print $1}')
    kubectl logs $pod_name -n $namespace >> $results_file
    echo "Result have been appended to $results_file"
    kubectl delete -f $yaml_file --namespace $namespace

done

