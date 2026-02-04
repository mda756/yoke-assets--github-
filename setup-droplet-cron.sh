#!/bin/bash
# Setup script for droplet - run this on the droplet
# This will set up the cron job for automatic syncing

echo "=== Droplet Git Auto-Sync Setup ==="
echo ""

# Check if running as root
if [ "$EUID" -ne 0 ]; then
    echo "ERROR: This script must be run as root"
    exit 1
fi

REPO_PATH="/root/yoke-assets--github-"
SCRIPT_PATH="$REPO_PATH/sync-repo.sh"
CRON_SCHEDULE="*/15 * * * *"

# Check if repository exists
if [ ! -d "$REPO_PATH" ]; then
    echo "Repository not found at $REPO_PATH"
    echo "Would you like to clone it now? (y/n)"
    read -r response
    if [ "$response" = "y" ] || [ "$response" = "Y" ]; then
        echo "Cloning repository..."
        cd /root || exit 1
        git clone git@github.com:mda756/yoke-assets--github-.git
        if [ $? -ne 0 ]; then
            echo "ERROR: Failed to clone repository"
            echo "Make sure SSH keys are set up for GitHub"
            exit 1
        fi
    else
        echo "Setup aborted"
        exit 1
    fi
fi

# Make sync script executable
if [ -f "$SCRIPT_PATH" ]; then
    chmod +x "$SCRIPT_PATH"
    echo "Made sync script executable"
else
    echo "ERROR: Sync script not found at $SCRIPT_PATH"
    echo "Make sure the repository is up to date"
    exit 1
fi

# Setup cron job
echo "Setting up cron job..."

# Remove existing cron job if present
crontab -l 2>/dev/null | grep -v "sync-repo.sh" | crontab -

# Add new cron job
(crontab -l 2>/dev/null; echo "$CRON_SCHEDULE $SCRIPT_PATH >> /root/yoke-assets-sync.log 2>&1") | crontab -

echo ""
echo "Cron job added successfully!"
echo "Schedule: Every 15 minutes"
echo "Script: $SCRIPT_PATH"
echo "Log file: /root/yoke-assets-sync.log"
echo ""
echo "Current crontab:"
crontab -l
echo ""
echo "To test the sync script manually, run:"
echo "  $SCRIPT_PATH"
echo ""
echo "To view the log:"
echo "  tail -f /root/yoke-assets-sync.log"
