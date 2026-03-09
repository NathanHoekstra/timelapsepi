#!/bin/bash
set -e

SERVICE_NAME=timelapsepi.service

# Detect repo directory
PROJECT_DIR="$(cd "$(dirname "$0")" && pwd)"

# Detect the real user even if sudo is used
USER_NAME="${SUDO_USER:-$(whoami)}"

echo "Project directory: $PROJECT_DIR"
echo "Installing service for user: $USER_NAME"

TMP_SERVICE=$(mktemp)

# Replace placeholder with actual path
sed -e "s|{{PROJECT_DIR}}|$PROJECT_DIR|g" \
    -e "s|{{USER}}|$USER_NAME|g" \
    systemd/$SERVICE_NAME.template > "$TMP_SERVICE"

echo "Installing systemd service..."

sudo cp "$TMP_SERVICE" /etc/systemd/system/$SERVICE_NAME

sudo systemctl daemon-reload
sudo systemctl enable $SERVICE_NAME
sudo systemctl restart $SERVICE_NAME

rm "$TMP_SERVICE"

echo "Service installed and started."
