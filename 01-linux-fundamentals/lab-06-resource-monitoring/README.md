# Lab 06 — Linux Resource Monitoring

## Objective
Build a Bash script that monitors Linux system resources and reports health conditions.

## Features
- System hostname, date, and uptime
- Logical CPU count and load averages
- RAM and swap statistics
- Root filesystem disk usage
- Automatic CPU load, memory, and disk health checks

## Tools Used
- Bash
- uptime
- nproc
- free
- df
- awk
- /proc/loadavg

## Running the Script

```bash
chmod +x resource-monitor.sh
./resource-monitor.sh


```

## Health Thresholds

| Metric | Warning | Critical |
|---|---|---|
| Disk usage | 80% | 90% |
| Estimated memory pressure | 80% | 90% |
| Normalized CPU load | 80% | 100% |

Normalized CPU load is not the same as CPU utilization.

## Kubernetes Relevance
Understanding CPU load, memory availability, and disk usage helps diagnose node resource problems, investigate performance bottlenecks, and troubleshoot workloads.

This lab uses simplified monitoring thresholds for learning purposes.
