#!/usr/bin/env bash

echo "=================================="
echo "    LINUX RESOURCE MONITOR"
echo "=================================="

echo
echo "Hostname: $(hostname)"
echo "Date: $(date)"
echo "Uptime:"
uptime

echo
echo "========== CPU =========="
echo "Logical CPUs: $(nproc)"

echo
echo "========== MEMORY =========="
free -h

echo
echo "========== DISK =========="
df -h /

echo
echo "========== DISK HEALTH CHECK =========="

DISK_USAGE=$(df / | awk 'NR==2 {gsub(/%/, "", $5); print $5}')

if [ "$DISK_USAGE" -ge 90 ]; then
    echo "CRITICAL: Disk usage is ${DISK_USAGE}%"
elif [ "$DISK_USAGE" -ge 80 ]; then
    echo "WARNING: Disk usage is ${DISK_USAGE}%"
else
    echo "OK: Disk usage is ${DISK_USAGE}%"
fi


echo
echo "========== MEMORY HEALTH CHECK =========="

MEMORY_USED=$(free | awk '/^Mem:/ {printf "%.0f", (1 - $7/$2) * 100}')

if [ "$MEMORY_USED" -ge 90 ]; then
    echo "CRITICAL: Memory pressure is ${MEMORY_USED}%"
elif [ "$MEMORY_USED" -ge 80 ]; then
    echo "WARNING: Memory pressure is ${MEMORY_USED}%"
else
    echo "OK: Memory pressure is ${MEMORY_USED}%"
fi

echo
echo "========== CPU LOAD HEALTH CHECK =========="

CPU_COUNT=$(nproc)
LOAD_1MIN=$(awk '{print $1}' /proc/loadavg)

LOAD_PERCENT=$(awk -v current_load="$LOAD_1MIN" -v cpus="$CPU_COUNT" \
    'BEGIN {printf "%.0f", (current_load / cpus) * 100}')

if [ "$LOAD_PERCENT" -ge 100 ]; then
    echo "CRITICAL: Normalized CPU load is ${LOAD_PERCENT}%"
elif [ "$LOAD_PERCENT" -ge 80 ]; then
    echo "WARNING: Normalized CPU load is ${LOAD_PERCENT}%"
else
    echo "OK: Normalized CPU load is ${LOAD_PERCENT}%"
fi
