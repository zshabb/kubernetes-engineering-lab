# Lab 01 — Kubernetes Resource Requests, Limits, and QoS

## Objective

Configure Kubernetes CPU and memory requests and limits, monitor actual resource consumption, reproduce an OOMKilled failure, and investigate Kubernetes Quality of Service classifications.

## Environment

- Kubernetes v1.35.0
- Three-node kind cluster
- kubectl
- Metrics Server
- Nginx Alpine
- Stress testing container

## Kubernetes Manifests

| File | Purpose |
|---|---|
| `deployment.yaml` | Two-replica Nginx Deployment with CPU and memory requests and limits |
| `oom-test.yaml` | Memory stress test demonstrating OOMKilled |
| `guaranteed-test.yaml` | Pod demonstrating Guaranteed QoS |

## Exercises Completed

1. Created a Deployment with two replicas and explicit CPU and memory requests and limits.
2. Verified Kubernetes scheduled the replicas across worker nodes.
3. Inspected node-level resource allocation using `kubectl describe node`.
4. Installed Metrics Server to enable resource monitoring.
5. Diagnosed kubelet TLS certificate validation failures.
6. Configured Metrics Server for the local kind environment.
7. Measured actual CPU and memory consumption using `kubectl top pods` and `kubectl top nodes`.
8. Created a memory stress-test Pod with a 64Mi memory limit.
9. Triggered an OOMKilled failure and confirmed exit code 137.
10. Investigated container termination details using `kubectl describe pod`.
11. Compared Burstable and Guaranteed QoS configurations.
12. Created a Pod with matching CPU and memory requests and limits and verified its Guaranteed QoS classification.

## Key Findings

- Kubernetes schedules Pods based on resource requests rather than actual utilization.
- CPU limits generally result in throttling when exceeded.
- Memory limits can cause container termination.
- An OOMKilled container commonly reports exit code 137.
- Metrics Server provides recent CPU and memory utilization through the Kubernetes Metrics API.
- Guaranteed QoS requires matching CPU and memory requests and limits for every container.
- Guaranteed QoS does not prevent a container from being OOMKilled.

## Production Considerations

- Size resource requests using observed application utilization and workload requirements.
- Account for memory spikes during application startup and peak traffic.
- Investigate repeated OOMKills before simply increasing memory limits.
- Avoid disabling kubelet TLS verification in production.
- Use resource monitoring and capacity planning to prevent scheduling failures.
- Consider Vertical Pod Autoscaler and Horizontal Pod Autoscaler for appropriate workloads.

## Result

Successfully deployed resource-managed applications, enabled Kubernetes resource monitoring, reproduced and diagnosed an OOMKilled failure, and verified Guaranteed QoS behavior.