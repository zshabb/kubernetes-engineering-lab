# Preemption investigation (optional)

Inspect the two PriorityClasses:

```bash
kubectl get priorityclass ai-interactive ai-batch
kubectl -n ai-team-a get pods -o custom-columns=NAME:.metadata.name,PRIORITY:.spec.priority,PHASE:.status.phase
kubectl -n ai-team-b get pods -o custom-columns=NAME:.metadata.name,PRIORITY:.spec.priority,PHASE:.status.phase
```

Preemption is **not** guaranteed just because a high-priority Pod exists. It requires an unschedulable high-priority Pod that could fit if lower-priority Pods were removed, subject to node constraints and PodDisruptionBudgets. This lab does not deliberately evict existing workloads on your shared kind cluster.

In a dedicated disposable cluster, experiment with lowering allocatable CPU and filling it with lower-priority Pods, then introduce a higher-priority Pod. Inspect `kubectl describe pod` events and scheduler decisions. Do not use this method on production nodes.
