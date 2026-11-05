# Linux Process Monitoring & Management

A Bash-based Linux process monitoring and signal management utility, developed as part of a hands-on Kubernetes engineering lab.

## Features

- Display the top five CPU-consuming processes
- Display the top five memory-consuming processes
- Summarize running, sleeping, and zombie process counts
- Inspect an individual process by PID
- Request process termination using SIGTERM
- Require interactive confirmation before termination
- Validate PID input and report errors through exit codes

## Requirements

- Linux
- Bash
- Standard Linux utilities: ps, sed, awk, kill

## Usage

Make the script executable:

    chmod +x process-monitor.sh

Display system-wide process information:

    ./process-monitor.sh

Inspect a process:

    ./process-monitor.sh 1234

Request termination:

    ./process-monitor.sh --terminate 1234

The termination command displays process details and requires confirmation before sending SIGTERM.

## Testing

The utility was manually tested in Ubuntu running under WSL2.

Validated scenarios:

- CPU and memory process listings
- Process state reporting
- PID inspection
- Invalid PID rejection
- SIGTERM termination of a temporary sleep process
- Cancellation of termination
- Interactive confirmation of termination

## Kubernetes Relevance

Understanding Linux processes and signals is essential for troubleshooting containerized workloads.

Kubernetes relies on process lifecycle management, exit codes, and termination signals to manage application containers.

## Limitations

This is an educational utility, not a production process supervisor.

- Process IDs can be reused between inspection and termination.
- Interactive confirmation does not eliminate all termination risks.
- Process state information is a point-in-time snapshot.
- Signal delivery is subject to Linux permissions.
- The script does not provide continuous monitoring or historical metrics.
