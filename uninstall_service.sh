#!/bin/bash
set -e

SERVICE_NAME=timelapsepi.service
SERVICE_PATH=/etc/systemd/system/$SERVICE_NAME

echo "Uninstalling $SERVICE_NAME..."

# Stop service if running
if systemctl is-active --quiet $SERVICE_NAME; then
    echo "Stopping service..."
    sudo systemctl stop $SERVICE_NAME
fi

# Disable service if enabled
if systemctl is-enabled --quiet $SERVICE_NAME 2>/dev/null; then
    echo "Disabling service..."
    sudo systemctl disable $SERVICE_NAME
fi

# Remove service file if it exists
if [ -f "$SERVICE_PATH" ]; then
    echo "Removing service file..."
    sudo rm "$SERVICE_PATH"
fi

echo "Reloading systemd..."
sudo systemctl daemon-reload

echo "Uninstall complete."
