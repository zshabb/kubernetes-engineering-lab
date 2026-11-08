# Lab 05 — Linux System Services and systemd

## Objective

Learn how Linux manages system services using systemd, including
service lifecycle management, dependencies, logging, and timers.

## Environment

- Ubuntu Linux on WSL2
- systemd as PID 1
- Bash

## Topics Covered

- Linux processes vs. system services
- systemd units and service configuration
- Service states: active, inactive, and failed
- Automatic startup and systemd targets
- Service dependencies: Requires and Wants
- systemd timers and one-shot services
- Service logs using journalctl
- Service restart policies
- Creating and installing a custom systemd service

## Custom Service

Created a Bash script named `service-check.sh` and a systemd
unit file named `service-check.service`.

The service:
1. Executes a Bash script using systemd.
2. Runs as the non-root user `pullz`.
3. Prints execution time and username.
4. Exits successfully using Type=oneshot.
5. Records output in the systemd journal.

## Commands Practiced

- systemctl list-units --type=service --state=running
- systemctl status cron
- systemctl is-enabled cron
- systemctl cat cron
- systemctl --failed
- systemctl show cron
- systemctl get-default
- systemctl list-dependencies graphical.target
- systemctl list-timers
- systemd-analyze verify service-check.service
- sudo systemctl daemon-reload
- sudo systemctl start service-check.service
- journalctl -u service-check.service -n 15 --no-pager

## Kubernetes Relevance

Kubernetes nodes commonly use systemd to manage services
such as kubelet and containerd.

Understanding systemd helps engineers troubleshoot node
services, inspect failures, analyze logs, and configure
reliable service startup.

## Result

Successfully created, installed, executed, and inspected
a custom systemd one-shot service.
