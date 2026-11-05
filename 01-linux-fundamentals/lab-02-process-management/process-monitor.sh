#!/usr/bin/env bash
set -euo pipefail

echo "=================================="
echo " Linux Process Monitor"
echo "=================================="
echo "Hostname: $(hostname)"
echo "Timestamp: $(date)"
echo

echo "=== Top 5 CPU Processes ==="
ps aux --sort=-%cpu | sed -n "1,6p"
echo

echo "=== Top 5 Memory Processes ==="
ps aux --sort=-%mem | sed -n "1,6p"
echo

echo "=== Process State Summary ==="
ps -eo stat= | awk '
{
    total++
    state = substr($1, 1, 1)
    if (state == "R") running++
    if (state == "S") sleeping++
    if (state == "Z") zombies++
}
END {
    printf "Total:    %d\n", total
    printf "Running:  %d\n", running
    printf "Sleeping: %d\n", sleeping
    printf "Zombies:  %d\n", zombies
}'

inspect_pid() {
    local pid="$1"

    if [[ ! "$pid" =~ ^[0-9]+$ ]]; then
        echo "Error: PID must be a positive integer." >&2
        return 1
    fi

    if ! ps -p "$pid" > /dev/null 2>&1; then
        echo "Error: Process $pid does not exist or is not accessible." >&2
        return 1
    fi

    echo
    echo "=== Process Details: PID $pid ==="
    ps -o pid,ppid,user,stat,%cpu,%mem,rss,etime,comm -p "$pid"
}

if [[ $# -gt 0 && "${1:-}" != "--terminate" ]]; then
    inspect_pid "$1"
fi

terminate_pid() {
    local pid="$1"

    if [[ ! "$pid" =~ ^[1-9][0-9]{0,9}$ ]] || [[ "$pid" == "1" ]]; then
        echo "Error: Invalid or protected PID." >&2
        return 1
    fi

    if [[ "$pid" == "$$" || "$pid" == "$PPID" ]]; then
        echo "Error: Refusing to terminate the current shell or parent." >&2
        return 1
    fi

    if ! ps -p "$pid" > /dev/null 2>&1; then
        echo "Error: Process $pid not found." >&2
        return 1
    fi

    echo "=== Process selected for termination ==="
    ps -o pid,ppid,user,stat,comm -p "$pid"

    local confirmation
    read -r -p "Send SIGTERM to PID $pid? [y/N]: " confirmation

    if [[ "$confirmation" != "y" && "$confirmation" != "Y" ]]; then
        echo "Termination cancelled."
        return 0
    fi

    echo "Sending SIGTERM to PID $pid..."
    kill -TERM "$pid"
}

if [[ "${1:-}" == "--terminate" ]]; then
    if [[ $# -ne 2 ]]; then
        echo "Usage: $0 --terminate PID" >&2
        exit 1
    fi
    terminate_pid "$2"
fi
