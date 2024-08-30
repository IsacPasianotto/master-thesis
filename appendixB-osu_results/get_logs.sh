#!/bin/bash 

yaml_file="./latency_mp_same_pod.yaml"
results_file="latency_mp_same_pod.txt"
targetpodname="latencymp-samepod"
namespace="osu"
niteration=30

if [ -z "$(kubectl get namespace $namespace)" ]; then
    echo "The namespace $namespace does not exist. Please create it first."
    exit 1
fi

for i in $(seq 1 $niteration); do
	status=""
	kubectl apply -f $yaml_file --namespace=$namespace

	while [ "$status" != "Completed" ]; do
	  status=$(kubectl get pod -n $namespace | grep $targetpodname | awk '{print $3}')
	  echo "Waiting for the benchmark to complete..."
	  sleep 1
	done

	pod_name=$(kubectl get pods -n $namespace | grep $targetpodname | awk '{print $1}')
	kubectl logs $pod_name -n $namespace >> $results_file

	echo "Result have been appended to $results_file"

	# Delete the job to reschedule it 
	kubectl delete -f $yaml_file --namespace $namespace
done
