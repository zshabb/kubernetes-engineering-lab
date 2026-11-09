#!/usr/bin/env bash
set -euo pipefail
EXPECTED_CONTEXT="kind-k8s-network-lab"
CURRENT_CONTEXT="$(kubectl config current-context)"
if [[ "$CURRENT_CONTEXT" != "$EXPECTED_CONTEXT" ]]; then
  echo "ERROR: context is $CURRENT_CONTEXT; expected $EXPECTED_CONTEXT" >&2
  exit 1
fi
for ns in ai-team-a ai-team-b; do
  kubectl get namespace "$ns" >/dev/null
  kubectl -n "$ns" get resourcequota tenant-budget >/dev/null
  kubectl -n "$ns" get limitrange container-defaults >/dev/null
  echo "PASS namespace, quota and limits: $ns"
done
kubectl get priorityclass ai-interactive ai-batch >/dev/null
echo 'PASS priority classes'
kubectl -n ai-team-a get deployment interactive-inference >/dev/null
kubectl -n ai-team-b get deployment batch-training >/dev/null
kubectl -n ai-team-a get pod gpu-training >/dev/null
echo 'PASS workload resources created'
echo 'GPU Pod state (Pending is expected without NVIDIA hardware):'
kubectl -n ai-team-a get pod gpu-training -o wide
echo 'Quota usage:'
kubectl -n ai-team-a describe resourcequota tenant-budget
kubectl -n ai-team-b describe resourcequota tenant-budget
