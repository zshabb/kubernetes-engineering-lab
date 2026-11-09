# Lab 04 — In-Cluster GPUWorkload Operator

Educational, **not production-ready** Kubernetes operator. Watches `GPUWorkload` custom resources, creates missing GPU Jobs, checks owner references, and reports drift **without deleting running or Pending Jobs**. Works on CPU-only kind: GPU Pods remain Pending.

## Prerequisite

Lab 03 CRD (`gpuworkloads.training.example.com`) installed in the kind cluster. Use the existing `gpuworkload.yaml` from Lab 03.

## Build and deploy (from this lab directory)

```bash
docker build -t gpuworkload-operator:lab04 ./controller
kind load docker-image gpuworkload-operator:lab04 --name k8s-network-lab
kubectl apply -f k8s/rbac.yaml
kubectl apply -f k8s/deployment.yaml
kubectl rollout status deployment/gpuworkload-operator --timeout=120s
kubectl logs deployment/gpuworkload-operator --tail=50
```

**Important:** The existing `h100-inference-job` created by Lab 03 may have a different owner reference or be out of sync. The operator will log an ownership mismatch or drift rather than taking it over or deleting it. For a clean test, manually delete **only the disposable lab Job** and let the operator recreate it:

```bash
kubectl delete job h100-inference-job --cascade=foreground --wait=true
kubectl get jobs -w
```

Stop the watch with Ctrl+C. Confirm owner reference:

```bash
kubectl get job h100-inference-job -o jsonpath='{.metadata.ownerReferences[0].kind}{" "}{.metadata.ownerReferences[0].name}{"\n"}'
```

Test watch-driven reconciliation by changing `gpuCount` in Lab 03's custom resource, applying it, and checking logs. The operator logs drift and does **not** replace the Job.

## Run unit tests

```bash
cd controller
python -m pip install -r requirements.txt
python -m unittest discover -v
```

## Security and limits

- Namespace-scoped Role and ServiceAccount; no cluster-admin.
- Single replica with `Recreate` strategy, **not** distributed leader election.
- Non-root container, read-only filesystem, dropped capabilities.
- The watch restarts after errors and periodically relists resources.
- This educational operator does not reconcile deletions of Jobs unless a `GPUWorkload` event or relist occurs; a 30-second resync supplies eventual recovery.
- No automatic Job replacement or GPU hardware dependency.
- For production: add leader election, structured status conditions, metrics, rate-limited workqueue, Kubernetes API conflict handling, robust watch resourceVersion management, and thorough integration tests.
