# Lab 05 — GPU Observability (Simulated)

Local kind learning stack: synthetic DCGM-style exporter → Prometheus → Grafana. **No NVIDIA GPU is used; these are simulated readings, not real DCGM measurements.** Prometheus is configured with alerts but no Alertmanager notifications. No Kubernetes-wide metrics are scraped; this lab focuses on GPU-style metrics.

## Install

From the lab directory:

```bash
python -m unittest discover -s tests -v
docker build -t gpu-metrics-simulator:lab05 simulator
kind load docker-image gpu-metrics-simulator:lab05 --name k8s-network-lab
kubectl apply -f k8s/namespace.yaml
kubectl apply -f k8s/simulator.yaml -f k8s/prometheus-config.yaml -f k8s/prometheus.yaml -f k8s/grafana-config.yaml -f k8s/grafana-dashboard.yaml -f k8s/grafana.yaml
kubectl -n gpu-observability rollout status deploy/simulated-dcgm --timeout=180s
kubectl -n gpu-observability rollout status deploy/prometheus --timeout=180s
kubectl -n gpu-observability rollout status deploy/grafana --timeout=180s
kubectl -n gpu-observability get pods
```

## View

In two separate terminals:

```bash
kubectl -n gpu-observability port-forward svc/grafana 3000:3000
kubectl -n gpu-observability port-forward svc/prometheus 9090:9090
```

Grafana: http://localhost:3000, login `admin` / `lab-only-change-me` (local lab only). Open **Dashboards → GPU Lab → GPU Observability (Simulated)**. Prometheus: http://localhost:9090/targets (target should be UP), http://localhost:9090/alerts.

## Validation

```bash
kubectl -n gpu-observability logs deploy/simulated-dcgm --tail=30
kubectl -n gpu-observability get pods,svc
kubectl -n gpu-observability get configmap
```

## Production differences

Replace synthetic exporter with NVIDIA GPU Operator DCGM Exporter on actual GPU nodes; use Prometheus Operator/ServiceMonitor, persistent TSDB storage, Alertmanager routing, secured Grafana credentials and ingress, TLS, SSO, HA and retention policies. The local lab uses ephemeral Prometheus storage and a deliberately lab-only Grafana password. Do not expose these services publicly.
