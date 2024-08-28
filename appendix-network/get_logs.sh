#!/bin/bash 

if [ -z "$(kubectl get namespace $namespace)" ]; then
    echo "The namespace $namespace does not exist. Please create it first."
    exit 1
fi

if [ $# -lt 4 ]; then
    echo "Wrong number of arguments provided!"
    echo "usage: $0 <yaml_file> <results_file> <target_pod_name> <namespace>"
    exit 1
fi

if [ ! -f $1 ]; then
    echo "The file $1 does not exist."
    exit 1
fi

yaml_file=$1
results_file=$2
targetpodname=$3
namespace=$4
status=""

kubectl apply -f $yaml_file --namespace=$namespace

while [ "$status" != "Completed" ]; do
  status=$(kubectl get pod -n $namespace | grep $targetpodname | awk '{print $3}')
  echo "Waiting for the benchmark to complete..."
  sleep 10
done

pod_name=$(kubectl get pods -n $namespace | grep $targetpodname | awk '{print $1}')
kubectl logs $pod_name -n $namespace >> $results_file
echo "Result have been appended to $results_file"
kubectl delete -f $yaml_file --namespace $namespace

