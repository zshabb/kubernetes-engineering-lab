#!/usr/bin/env bash
set -euo pipefail
kubectl delete -f examples/gpu-pod.yaml --ignore-not-found
