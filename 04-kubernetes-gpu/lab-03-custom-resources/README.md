# Lab 03 — Kubernetes Custom Resources and GPU Controller

## Objective

Build a Python Kubernetes controller that manages GPU Jobs using a custom `GPUWorkload` resource.

## Technologies

- Kubernetes
- Python
- Kubernetes Python Client
- Custom Resource Definitions (CRDs)
- Kubernetes Jobs
- Owner References
- Kubernetes API validation

## Architecture

`GPUWorkload CRD → Python Controller → Kubernetes Job → GPU Pod`

## Features

- Custom GPUWorkload resource with schema validation
- Kubernetes Job creation
- GPU resource allocation requests
- Configuration drift detection for GPU count and image
- Owner Reference verification
- Pending Pod safety checks
- Explicit replacement approval
- Foreground Job deletion and recreation
- Duplicate Job prevention

## Usage

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

Run a reconciliation pass:

```bash
python controller.py
```

Approve replacement of an eligible Pending Job:

```bash
python controller.py --approve-replacement
```

## Testing

Tested on a three-node kind Kubernetes cluster without physical NVIDIA GPUs.

The controller successfully created GPU-requesting Jobs, detected configuration drift, and prevented unauthorized replacement.

GPU Pods remain Pending because the cluster does not advertise NVIDIA GPU resources.

## Limitations

This is an educational controller, not a production-ready Operator. It does not implement continuous reconciliation, leader election, full concurrency protection, or comprehensive lifecycle management.

## Skills Demonstrated

Kubernetes API extensions, custom controller development, desired-state reconciliation, resource ownership, scheduling diagnostics, and safe workload management.
