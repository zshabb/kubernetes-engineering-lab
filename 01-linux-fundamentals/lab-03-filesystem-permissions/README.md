# Lab 03 — Linux Filesystems & Permissions

## Objective
Understand Linux filesystem permissions, ownership,
inodes, links, mount points, and filesystem security.

## Concepts Practiced
- File and directory permissions (chmod)
- User and group ownership (chown, chgrp)
- UID and GID
- Default permissions using umask
- Inodes and hard links
- Symbolic links and broken links
- Filesystem mounts (df, findmnt)
- Bash scripting and error handling

## Filesystem Inspector

A Bash utility that displays:
- Current user and UID/GID
- Target file permissions
- File ownership
- Inode number
- Filesystem type and mount options

## Usage

Run from this lab directory:

    ./filesystem-inspector.sh test-file.txt

Inspect a directory:

    ./filesystem-inspector.sh secure-dir

Inspect the current directory:

    ./filesystem-inspector.sh

## Error Handling

Invalid targets produce an error message and
exit with a nonzero status.

## Kubernetes Relevance

These concepts help troubleshoot:
- Container permission errors
- PersistentVolume access
- Security contexts (runAsUser, runAsGroup, fsGroup)
- Read-only volume mounts
- File ownership and group permissions
