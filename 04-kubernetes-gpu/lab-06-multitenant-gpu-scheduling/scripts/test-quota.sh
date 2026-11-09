#!/usr/bin/env bash
set -euo pipefail
if [[ "$(kubectl config current-context)" != 'kind-k8s-network-lab' ]]; then
  echo 'ERROR: wrong Kubernetes context' >&2
  exit 1
fi
# Server-side dry-run exercises the API server admission chain without persisting a Pod.
output="$(kubectl -n ai-team-a create --dry-run=server -f - 2>&1 <<'YAML'
apiVersion: v1
kind: Pod
metadata:
  name: quota-denial-probe
spec:
  containers:
    - name: probe
      image: busybox:1.36
      command: ["sleep", "60"]
      resources:
        requests:
          cpu: "3"
          memory: 64Mi
        limits:
          cpu: "3"
          memory: 128Mi
YAML
)" && rc=0 || rc=$?
if [[ "$rc" -eq 0 ]]; then
  echo 'FAIL: quota did not reject oversized request' >&2
  exit 1
fi
if grep -Eqi 'exceeded quota|resourcequota|quota' <<<"$output"; then
  echo 'PASS: API server denied oversized CPU request due to quota'
  echo "$output"
else
  echo 'FAIL: admission failed for a reason other than quota:' >&2
  echo "$output" >&2
  exit 1
fi
