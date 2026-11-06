# Lab 04 — Linux Networking Fundamentals

## Objective

Understand Linux networking and build a Bash-based
network diagnostics tool for infrastructure troubleshooting.

## Skills Practiced

- Network interfaces and IPv4 addressing
- CIDR notation and subnetting
- Routing tables and default gateways
- DNS resolution and resolver configuration
- TCP and UDP sockets
- Listening ports and network services
- HTTP/HTTPS and TLS connectivity
- Linux networking troubleshooting
- Bash scripting and exit-status handling

## Commands Used

| Command | Purpose |
|---------|---------|
| ip -br addr | Inspect network interfaces |
| ip route | Display routing table |
| ip route get | Determine packet routing |
| ping | Test ICMP connectivity |
| getent ahostsv4 | Resolve IPv4 addresses |
| ss -tuln | Inspect listening ports |
| curl -v | Diagnose HTTP/HTTPS connections |

## Project: Network Diagnostics Script

The `network-diagnostics.sh` script:

1. Displays network interfaces and IP addresses.
2. Displays the routing table.
3. Shows DNS resolver configuration.
4. Lists listening TCP and UDP sockets.
5. Tests external IP connectivity.
6. Tests DNS resolution.
7. Tests HTTPS connectivity.

## Usage

```bash
chmod +x network-diagnostics.sh
./network-diagnostics.sh
