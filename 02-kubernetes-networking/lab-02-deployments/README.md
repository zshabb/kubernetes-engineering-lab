# Lab 02 — Kubernetes Deployments and Rolling Updates

## Objective
Deploy a replicated application, expose it through a Kubernetes Service, test self-healing and load balancing, and practice rolling updates and rollback.

## Environment
- Kubernetes v1.35.0
- Three-node kind cluster
- Nginx
- kubectl

## Kubernetes Resources
- `deployment.yaml` — Three-replica Nginx Deployment with an explicit rolling update strategy.
- `service.yaml` — ClusterIP Service exposing the application internally.

## Exercises Completed
1. Created a three-replica Nginx Deployment using YAML.
2. Verified Pod placement across worker nodes.
3. Deleted a Pod and observed automatic replacement.
4. Created a ClusterIP Service targeting the Deployment.
5. Inspected EndpointSlices to confirm all three replicas were registered.
6. Sent HTTP requests through the Service and inspected Nginx logs to verify traffic reached multiple replicas.
7. Configured `maxSurge: 1` and `maxUnavailable: 0`.
8. Updated Nginx from `nginx:alpine` to `nginx:1.28-alpine`.
9. Verified rollout completion and inspected ReplicaSets and revision history.
10. Rolled back to the previous version and verified the restored image.
11. Synchronized the declarative YAML with the live Deployment.

## Kubernetes Skills Demonstrated
- Deployments and ReplicaSets
- Replica management and self-healing
- Service load balancing
- Rolling updates
- Deployment revision history
- Rollback and recovery
- Declarative configuration management

## Key Takeaway
Kubernetes Deployments maintain the desired replica count and support controlled application updates. Rolling updates and rollbacks help restore service during deployments, while keeping YAML synchronized with the cluster prevents configuration drift.

## Production Considerations
Use immutable container image digests, readiness probes, resource requests and limits, and version-controlled manifests for reliable production deployments.
