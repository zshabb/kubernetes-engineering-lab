
#!/usr/bin/env bash
set -euo pipefail

echo "================================="
echo "       LINUX SYSTEM REPORT"
echo "================================="

echo
echo "=== Hostname ==="
hostname

echo
echo "=== Kernel ==="
uname -r

echo
echo "=== Operating System ==="
cat /etc/os-release | grep PRETTY_NAME

echo
echo "=== CPU ==="
lscpu | grep -E 'Architecture:|CPU\(s\):|Model name:'

echo
echo "=== Memory ==="
free -h

echo
echo "=== Disk Usage ==="
df -h /

echo
echo "=== Top Memory Processes ==="
ps aux --sort=-%mem | head -n 6

echo
echo "=== System Uptime ==="
uptime

echo
echo "Report completed."
