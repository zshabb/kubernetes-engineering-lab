#!/usr/bin/env bash

SERVICE_NAME="${1:-cron}"
MAX_ATTEMPTS=5
ATTEMPT=1

check_service() {
    systemctl is-active --quiet "$SERVICE_NAME"
}

echo "Checking service: $SERVICE_NAME"

while [ "$ATTEMPT" -le "$MAX_ATTEMPTS" ]; do

    echo "Attempt $ATTEMPT of $MAX_ATTEMPTS"

    if check_service; then
        echo "SUCCESS: $SERVICE_NAME is running"
        exit 0
    fi

    ATTEMPT=$((ATTEMPT + 1))

    if [ "$ATTEMPT" -le "$MAX_ATTEMPTS" ]; then
        sleep 1
    fi

done

echo "ERROR: $SERVICE_NAME is not running"
exit 1
