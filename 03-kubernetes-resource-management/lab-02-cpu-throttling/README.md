# Lab 02 — Kubernetes CPU Throttling

## Objective

Investigate how Kubernetes CPU limits affect container CPU usage and throttling using Linux cgroup statistics.

## Environment

- Kubernetes kind cluster
- kubectl
- Metrics Server
- Linux cgroup v2
- CPU stress-test container

## Experiments

### Experiment 1 — 500m CPU Limit

Configured two CPU-intensive workers with a CPU limit of 500m.

Results:
- Actual CPU usage: 502m
- CPU quota: `50000 100000`
- Total enforcement periods: 1,213
- Throttled periods: 1,212
- Throttling frequency: 99.92%

### Experiment 2 — 2000m CPU Limit

Increased the CPU limit to 2000m.

Results:
- Actual CPU usage: 1996m
- CPU quota: `200000 100000`
- Total enforcement periods: 1,253
- Throttled periods: 214
- Throttling frequency: 17.08%

The throttling frequency decreased by approximately 82.84 percentage points.

### Experiment 3 — No CPU Limit

Removed the CPU limit while retaining a 100m CPU request.

Verified the cgroup CPU quota:

`max 100000`

This confirms that no CPU quota is configured at the Pod's CPU cgroup level.

## Commands Used

- `kubectl top pod cpu-test`
- `kubectl exec cpu-test -- cat /sys/fs/cgroup/cpu.stat`
- `kubectl exec cpu-test -- cat /sys/fs/cgroup/cpu.max`
- `kubectl delete pod cpu-test`
- `kubectl apply -f cpu-test.yaml`

## Key Findings

- CPU requests influence scheduling and CPU allocation under contention.
- CPU limits enforce CPU-time quotas through Linux cgroups.
- Containers can remain healthy while experiencing substantial CPU throttling.
- Increasing CPU limits can reduce throttling when sufficient CPU capacity is available.
- Removing a CPU limit does not guarantee exclusive access to CPU cores.
- Cumulative cgroup counters must be interpreted alongside their observation windows.

## Relevance to NVIDIA H100 Infrastructure

GPU workloads depend on CPU processing for request handling, tokenization, data preparation, and other operations.

Excessive CPU throttling can increase inference latency and reduce GPU utilization.

CPU limits should be configured using workload measurements rather than arbitrary values.

## Result

Successfully reproduced CPU throttling, inspected Linux cgroup CPU quotas, compared two CPU limits, and verified a configuration without a CPU limit.
