# Lab 07 — Bash Scripting and Automation

## Objective
Build a reusable Linux service health checker with retry logic and proper exit codes.

## Features
- Accepts a service name as a command-line argument
- Defaults to checking cron
- Uses a Bash function to check service status
- Retries failed checks up to five times
- Returns exit code 0 for success
- Returns exit code 1 for failure

## Technologies
- Bash
- systemctl
- systemd

## Usage

Check the default service:

    ./service-health-check.sh

Check a specific service:

    ./service-health-check.sh cron

Test the failure scenario:

    ./service-health-check.sh nonexistent-service

## Concepts Practiced
- Bash functions
- Positional arguments
- Local and global variables
- Conditional statements
- For and while loops
- Exit codes and error handling
- Retry logic

## Kubernetes Relevance
These scripting techniques are useful for automating infrastructure checks,
validating services, troubleshooting failures, and building operational tools.

Kubernetes also provides native startup, readiness, and liveness probes
for container health monitoring.
