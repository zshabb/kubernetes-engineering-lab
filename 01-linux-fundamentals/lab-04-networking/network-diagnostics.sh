#!/usr/bin/env bash

set -u

echo "================================"
echo "   Linux Network Diagnostics"
echo "================================"

echo
echo "=== Network Interfaces ==="
ip -br addr

echo
echo "=== Routing Table ==="
ip route

echo
echo "=== DNS Configuration ==="
cat /etc/resolv.conf

echo
echo "=== Listening TCP/UDP Ports ==="
ss -tuln

echo
echo "=== Internet Connectivity ==="

if ping -c 2 -W 2 8.8.8.8 > /dev/null 2>&1; then
    echo "[PASS] Internet IP connectivity"
else
    echo "[FAIL] Cannot reach 8.8.8.8"
fi

echo
echo "=== DNS Resolution ==="

if getent ahostsv4 google.com > /dev/null 2>&1; then
    echo "[PASS] DNS resolution working"
else
    echo "[FAIL] DNS resolution failed"
fi

echo
echo "=== HTTPS Connectivity ==="

if curl -fsS -o /dev/null --connect-timeout 3 --max-time 10 https://www.google.com; then
    echo "[PASS] HTTPS connectivity working"
else
    echo "[FAIL] HTTPS connectivity failed"
fi
