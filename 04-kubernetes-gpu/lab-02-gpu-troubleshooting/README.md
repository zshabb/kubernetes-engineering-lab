# Lab 02 — Kubernetes GPU Troubleshooting

## Objective

Build a reusable Bash script to diagnose GPU scheduling failures in Kubernetes.

## Environment

- Kubernetes v1.35.0
- Three-node kind cluster
- kubectl
- Bash

## Tool

`gpu-diagnose.sh` accepts a Pod name and namespace:

```bash
./gpu-diagnose.sh gpu-test default
```

The script collects:

1. Pod status and node assignment.
2. GPU resources advertised by Kubernetes nodes.
3. GPU limits requested by the Pod.
4. Kubernetes scheduling events.

## Investigation

The test Pod requested one NVIDIA GPU but remained Pending.

### Findings

- Pod status: Pending
- Assigned node: None
- GPU request: 1
- Advertised GPU resources: 0
- Scheduler reason: Insufficient `nvidia.com/gpu`

Node affinity and tolerations were also evaluated during scheduling.

## Root Cause

No eligible Kubernetes node advertised the required NVIDIA GPU resource.

The Pod could not be scheduled.

## Production Troubleshooting

On a real NVIDIA H100 cluster, additional checks would include:

- Physical GPU detection using `nvidia-smi`.
- NVIDIA driver health.
- NVIDIA GPU Operator status.
- Device Plugin DaemonSet readiness and logs.
- Kubelet device-plugin registration.
- Node Capacity and Allocatable GPU resources.
- Node affinity, taints, and tolerations.

## Result

Created and tested a reusable GPU scheduling diagnostic script that identifies missing GPU capacity and captures Kubernetes scheduler events.

The lab used a CPU-only kind cluster; no physical GPU was required.
