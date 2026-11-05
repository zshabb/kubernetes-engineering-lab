#!/usr/bin/env bash

echo "=== Linux Filesystem Inspector ==="
echo "Current user: $(whoami)"
echo "UID/GID: $(id -u):$(id -g)"
echo "Current directory: $(pwd)"

echo
echo "=== File Inspection ==="

TARGET="${1:-.}"

if [[ ! -e "$TARGET" && ! -L "$TARGET" ]]; then
    echo "ERROR: Target does not exist: $TARGET" >&2
    exit 1
fi

stat -c 'Name: %n | Permissions: %a (%A) | Owner: %U | Group: %G | Inode: %i' "$TARGET"

echo
echo "=== Filesystem Mount ==="

findmnt -T "$TARGET" -o TARGET,SOURCE,FSTYPE,OPTIONS
