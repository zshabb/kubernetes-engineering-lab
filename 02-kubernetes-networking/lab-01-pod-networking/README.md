# Lab 01 — Kubernetes Pod Networking

## Objective
Understand how Kubernetes Pods communicate across worker nodes and how ClusterIP Services provide stable networking.

## Environment
- Kubernetes v1.35.0
- kind (Kubernetes in Docker)
- One control-plane node and two worker nodes
- kubectl

## Exercises Completed
1. Created a three-node Kubernetes cluster using a declarative kind configuration.
2. Deployed Nginx and BusyBox Pods on separate worker nodes.
3. Verified cross-node Pod-to-Pod HTTP communication.
4. Created a ClusterIP Service for Nginx.
5. Verified Service DNS resolution and connectivity.
6. Inspected Service endpoints using EndpointSlices.
7. Simulated a broken Service selector and diagnosed the resulting connectivity failure.
8. Restored the correct selector and verified connectivity.

## Kubernetes Skills Demonstrated
- Pod networking
- Cross-node communication
- ClusterIP Services
- Kubernetes DNS
- Service selectors and EndpointSlices
- Network troubleshooting

## Key Takeaway
Pods can communicate across Kubernetes nodes, while Services provide stable network endpoints for dynamically changing Pods. Incorrect Service selectors can break connectivity even when application Pods remain healthy.
