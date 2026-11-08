# Lab 01 — Kubernetes GPU Scheduling

## Objective

Investigate Kubernetes GPU resource scheduling, node affinity, taints, and tolerations using a three-node kind cluster without physical GPU hardware.

## Environment

- Kubernetes v1.35.0
- Three-node kind cluster
- kubectl
- Simulated NVIDIA H100 node label

## Exercises Completed

1. Inspected node GPU resources using `kubectl get nodes`.
2. Created a Pod requesting `nvidia.com/gpu: 1`.
3. Investigated `FailedScheduling` events.
4. Verified that no worker advertised NVIDIA GPU resources.
5. Inspected node Capacity and Allocatable resources.
6. Labeled Worker 1 with `accelerator=nvidia-h100`.
7. Added required node affinity targeting H100-labeled nodes.
8. Verified the scheduler rejected nodes without the matching label.
9. Inspected the control-plane `NoSchedule` taint.
10. Added `dedicated=gpu:NoSchedule` to the simulated GPU worker.
11. Added a matching toleration to the GPU Pod.
12. Verified the toleration using the Kubernetes API.
13. Confirmed the remaining scheduling failure was insufficient GPU capacity.

## Key Concepts

### GPU Resource Discovery

NVIDIA GPU device plugins advertise GPU resources to Kubernetes using extended resources such as `nvidia.com/gpu`.

A node label alone does not provide GPU capacity.

### Node Affinity

Required node affinity restricts scheduling to nodes matching specified labels.

### Taints and Tolerations

Taints restrict which Pods may schedule onto a node.

Matching tolerations allow Pods to pass those restrictions but do not guarantee placement.

### Resource Availability

The Kubernetes scheduler must find sufficient allocatable resources on an eligible node.

### Production Relevance

These mechanisms support dedicated GPU node pools, AI inference placement, GPU workload isolation, and troubleshooting workloads that remain Pending.

## Result

Successfully configured and verified GPU scheduling constraints in a simulated H100 environment, including node affinity, taints, tolerations, and resource availability checks.

No physical NVIDIA GPU was installed or used in this lab.
