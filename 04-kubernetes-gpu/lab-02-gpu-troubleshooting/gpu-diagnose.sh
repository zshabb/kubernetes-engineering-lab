#!/usr/bin/env bash
set -euo pipefail

POD="${1:-gpu-test}"
NAMESPACE="${2:-default}"

echo "=== GPU Pod Diagnosis ==="
echo "Pod: $POD"
echo "Namespace: $NAMESPACE"
echo

echo "=== Pod Status ==="
kubectl get pod "$POD" -n "$NAMESPACE" -o wide
echo

echo "=== GPU Capacity by Node ==="
kubectl get nodes \
  -o custom-columns='NAME:.metadata.name,GPUS:.status.allocatable.nvidia\.com/gpu'
echo

echo "=== Pod Scheduling Requirements ==="
kubectl get pod "$POD" -n "$NAMESPACE" \
  -o jsonpath='GPU Limits: {.spec.containers[*].resources.limits.nvidia\.com/gpu}{"\n"}'
echo

echo "=== Scheduling Events ==="
kubectl get events -n "$NAMESPACE" \
  --field-selector "involvedObject.name=$POD" \
  --sort-by=.lastTimestamp
