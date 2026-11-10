#!/usr/bin/env bash
set -euo pipefail
printf '\n== Kubernetes context ==\n'
kubectl config current-context
printf '\n== Node GPU capacity and labels ==\n'
kubectl get nodes -o custom-columns='NAME:.metadata.name,GPU_CAPACITY:.status.capacity.nvidia\.com/gpu,GPU_ALLOCATABLE:.status.allocatable.nvidia\.com/gpu,MIG_LABEL:.metadata.labels.nvidia\.com/mig\.config' || true
printf '\n== NVIDIA resources on nodes (if any) ==\n'
kubectl get nodes -o json | python3 -c 'import json,sys; x=json.load(sys.stdin); [(print(n["metadata"]["name"], {k:v for k,v in n.get("status",{}).get("allocatable",{}).items() if k.startswith("nvidia.com/")})) for n in x["items"]]'
printf '\n== NVIDIA pods (if installed) ==\n'
kubectl get pods -A -o wide | grep -Ei 'nvidia|gpu-operator|dcgm|NAME' || true
printf '\n== GPU-request Pod status (if present) ==\n'
kubectl get pod lab07-gpu-request -o wide --ignore-not-found
