# Lab 06 — Multi-tenant GPU Scheduling

A reproducible kind-cluster lab demonstrating namespace isolation, ResourceQuota, LimitRange, PriorityClass, scheduling constraints, and a controlled CPU preemption experiment. No physical GPU is needed.

## Safety and scope
- Uses two dedicated namespaces, `ai-team-a` and `ai-team-b`.
- The optional preemption experiment uses a **dedicated tainted node** and temporarily creates CPU load; run only in a disposable kind cluster.
- GPU workloads are expected to remain Pending because kind has no NVIDIA GPU resource advertised. **Do not label a node as though it provides a real GPU**; labels are just metadata.
- PriorityClass alone does not guarantee preemption. The optional experiment shows how to inspect scheduling events without claiming preemption must occur.
- Kubernetes ResourceQuota is namespace-scoped; it does not provide physical GPU isolation, MIG partitioning, or fairness across teams.

## Quick start
From this lab directory:

```bash
kubectl config current-context  # must be kind-k8s-network-lab
kubectl apply -f k8s/00-priorityclasses.yaml
kubectl apply -f k8s/01-namespaces.yaml
kubectl apply -f k8s/02-quotas.yaml
kubectl apply -f k8s/03-limitranges.yaml
kubectl apply -f k8s/04-cpu-workloads.yaml
kubectl apply -f k8s/05-gpu-workloads.yaml
bash scripts/verify.sh
```

## What to observe

```bash
kubectl get resourcequota -n ai-team-a
kubectl get resourcequota -n ai-team-b
kubectl get pods -n ai-team-a -o wide
kubectl get pods -n ai-team-b -o wide
kubectl describe pod gpu-training -n ai-team-a
kubectl get priorityclass
```

CPU-based Pods should schedule normally unless the cluster is under resource pressure. GPU Pod `gpu-training` should remain Pending on a GPU-less cluster. Its scheduler events typically report `Insufficient nvidia.com/gpu`, possibly alongside other constraints.

## Test quota enforcement

```bash
bash scripts/test-quota.sh
```

The test submits a deliberately oversized CPU Pod to team A and expects an admission denial from ResourceQuota. It does not leave a Pod running.

## Optional: preemption investigation

See `scripts/preemption-notes.md`. Preemption is conditional, and we intentionally do not force a deterministic preemption scenario on your existing cluster.

## Cleanup

```bash
kubectl delete -f k8s/05-gpu-workloads.yaml --ignore-not-found
kubectl delete -f k8s/04-cpu-workloads.yaml --ignore-not-found
kubectl delete -f k8s/03-limitranges.yaml --ignore-not-found
kubectl delete -f k8s/02-quotas.yaml --ignore-not-found
kubectl delete -f k8s/01-namespaces.yaml --ignore-not-found
kubectl delete -f k8s/00-priorityclasses.yaml --ignore-not-found
```

Do not delete the existing `gpu-observability` namespace or your Lab 04 operator.
