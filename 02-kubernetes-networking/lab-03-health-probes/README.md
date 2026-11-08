# Lab 03 — Kubernetes Health Probes

## Objective

Configure and test Kubernetes readiness and liveness probes to understand how Kubernetes detects application failures and performs automatic recovery.

## Environment

- Kubernetes v1.35.0
- Three-node kind cluster
- Nginx Alpine
- kubectl

## Kubernetes Resources

- `deployment.yaml` — Two-replica Nginx Deployment with HTTP readiness and liveness probes.

## Exercises Completed

1. Created a Deployment with two Nginx replicas.
2. Configured an HTTP readiness probe checking `/` on port 80.
3. Verified both Pods became Ready.
4. Simulated an application failure by renaming the Nginx homepage.
5. Observed readiness failures returning HTTP 403.
6. Confirmed the affected Pod remained Running but became Not Ready, without restarting.
7. Restored the homepage and verified readiness recovered automatically.
8. Added an HTTP liveness probe and performed a rolling update.
9. Simulated another HTTP 403 failure.
10. Observed three consecutive liveness failures triggering an automatic container restart.
11. Verified the container recovered with one restart while retaining its Pod identity.
12. Inspected Kubernetes events to identify the failure and recovery sequence.

## Key Concepts

| Probe | Purpose | Behavior on Failure |
|---|---|---|
| Readiness | Determines whether a container can serve traffic | Marks the Pod Not Ready |
| Liveness | Determines whether a container needs restarting | Restarts the container |
| Startup | Allows slow-starting applications time to initialize | Restarts the container after its failure threshold |

## Production Lessons

- A Running Pod is not necessarily a healthy application.
- Readiness failures do not automatically restart containers.
- Liveness probes should detect conditions that restarting can resolve.
- Readiness probes protect Service traffic by excluding unready endpoints.
- `kubectl describe pod` provides valuable health-check and restart events.
- Health endpoints should reflect actual application health rather than simply checking whether a static file exists.

## Result

Successfully demonstrated readiness failure and recovery without a restart, followed by liveness-triggered container restart and automatic recovery.