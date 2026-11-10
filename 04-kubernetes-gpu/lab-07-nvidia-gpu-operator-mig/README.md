# Lab 07 — NVIDIA GPU Operator, MIG & time-slicing

## Goal
Understand the real NVIDIA GPU Operator architecture and validate GPU resource scheduling on a GPU-less local kind cluster. This lab **does not install** the NVIDIA GPU Operator, create MIG devices, or pretend labels represent GPU hardware.

## Architecture
NVIDIA GPU Operator coordinates GPU driver deployment, NVIDIA Container Toolkit, Kubernetes device plugin, GPU Feature Discovery, DCGM exporter, and MIG Manager on supported hosts. Node Feature Discovery (NFD) is a separate hardware-discovery component. Actual capabilities depend on hardware, drivers, runtime, and chart versions.

MIG divides compatible GPUs into hardware-isolated GPU instances with defined compute/memory resources. Time-slicing advertises multiple logical replicas of GPU resources and shares execution time; it is **not** equivalent to MIG memory/fault isolation. Do not assume time-slicing provides performance isolation.

## Local kind workflow
```bash
python3 -m unittest discover -s tests -v
bash scripts/inspect.sh
bash scripts/verify.sh
bash scripts/cleanup.sh
```

`verify.sh` only runs against a `kind-*` context. It creates a GPU-requesting Pod and confirms it remains Pending without GPU allocatable resources. It does not mutate nodes, install drivers, or change existing GPU Operator settings.

## Real GPU cluster preparation (NOT for kind)
Use NVIDIA's current documentation and Helm chart version compatible with your Kubernetes distribution, NVIDIA driver, and container runtime. Before installing, verify `nvidia-smi`, GPU model, driver version, node runtime, and operator compatibility. Common high-level workflow:

```bash
# Commands for a compatible GPU-equipped cluster only; review chart values first.
helm repo add nvidia https://helm.ngc.nvidia.com/nvidia
helm repo update
helm show values nvidia/gpu-operator > gpu-operator-values-review.yaml
# Review compatibility and values, then install using the official guide.
```

Do not apply the example ConfigMaps as production configuration. MIG configuration keys and supported profiles vary by GPU and operator version. On real hardware, enabling/disabling MIG or changing partitions can disrupt active GPU workloads; drain/coordinate before changes. H100 supports MIG but available profiles depend on device type and platform. The reference `all-enabled` configuration is illustrative and does not specify a usable partition layout.

## Investigation checklist
1. `kubectl get nodes -o json` — check `status.allocatable` for `nvidia.com/gpu` or MIG resource names.
2. Inspect GPU Operator and device-plugin Pods and their logs.
3. Check GPU Feature Discovery labels versus actual allocatable resources.
4. On GPU nodes, inspect `nvidia-smi -L` and `nvidia-smi mig -lgi` as supported.
5. For Pending Pods, inspect `kubectl describe pod` scheduling events.

## Portfolio evidence
Unit tests, inspection output, and a screenshot of the Pending GPU Pod scheduling event. The absence of hardware is an explicit test constraint, not proof that the real NVIDIA Operator works.
