#!/usr/bin/env bash
set -euo pipefail
CTX=$(kubectl config current-context)
if [[ "$CTX" != kind-* ]]; then
  echo "Refusing simulation on non-kind context: $CTX" >&2; exit 1
fi
kubectl apply -f examples/gpu-pod.yaml
sleep 3
PHASE=$(kubectl get pod lab07-gpu-request -o jsonpath='{.status.phase}')
if [[ "$PHASE" != Pending ]]; then
  echo "Unexpected phase $PHASE; inspect GPU capacity before continuing" >&2; exit 1
fi
echo "PASS: GPU request is Pending on GPU-less kind cluster"
kubectl get pod lab07-gpu-request -o wide
kubectl describe pod lab07-gpu-request | tail -25
