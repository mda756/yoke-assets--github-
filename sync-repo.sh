#!/bin/bash
# Git Auto-Sync Script for Droplet
# Logs activity and handles conflicts gracefully

REPO_PATH="/root/yoke-assets--github-"
LOG_PATH="/root/yoke-assets-sync.log"
CLAUDE_FOLDER="claude code creator"

log_message() {
    local message="$1"
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    echo "[$timestamp] $message" | tee -a "$LOG_PATH"
}

handle_merge_conflict() {
    log_message "Merge conflict detected. Attempting to resolve..."

    # Abort the current merge
    git merge --abort 2>/dev/null

    # Stash local changes
    log_message "Stashing local changes..."
    git stash push -m "Auto-stash before sync - $(date '+%Y-%m-%d %H:%M:%S')"

    # Pull again
    log_message "Pulling from origin after stash..."
    git pull origin main

    # Try to apply stash
    log_message "Attempting to re-apply stashed changes..."
    if ! git stash pop 2>&1; then
        log_message "Could not automatically re-apply changes. Changes are saved in stash."
        log_message "Manual intervention may be required."
        return 1
    fi

    return 0
}

# Change to repository directory
cd "$REPO_PATH" || {
    log_message "ERROR: Could not change to repository directory: $REPO_PATH"
    exit 1
}

log_message "=== Starting sync process ==="

# Check if we're in a git repository
if ! git rev-parse --git-dir &>/dev/null; then
    log_message "ERROR: Not a git repository"
    exit 1
fi

# Fetch latest changes
log_message "Fetching from origin..."
git fetch origin 2>&1 | tee -a "$LOG_PATH"

# Pull changes from origin
log_message "Pulling changes from origin..."
pull_output=$(git pull origin main 2>&1)
pull_exit_code=$?

if [ $pull_exit_code -ne 0 ] && echo "$pull_output" | grep -q "CONFLICT"; then
    if ! handle_merge_conflict; then
        log_message "Failed to handle merge conflict automatically"
        exit 1
    fi
elif [ $pull_exit_code -ne 0 ]; then
    log_message "ERROR during pull: $pull_output"
    exit 1
else
    log_message "Pull successful: $pull_output"
fi

# Check for changes in claude code creator folder
if [ -d "$CLAUDE_FOLDER" ]; then
    log_message "Checking for changes in '$CLAUDE_FOLDER' folder..."

    # Add all changes in claude code creator folder
    git add "$CLAUDE_FOLDER/" 2>&1 | tee -a "$LOG_PATH"

    # Check if there are staged changes
    if ! git diff --cached --quiet; then
        log_message "Found changes in '$CLAUDE_FOLDER'. Committing..."

        # Create commit message
        commit_message="Auto-sync: Updates to claude code creator folder - $(date '+%Y-%m-%d %H:%M:%S')"

        if git commit -m "$commit_message" 2>&1 | tee -a "$LOG_PATH"; then
            log_message "Commit successful"
        else
            log_message "ERROR: Commit failed"
            exit 1
        fi
    else
        log_message "No changes to commit in '$CLAUDE_FOLDER'"
    fi
else
    log_message "WARNING: '$CLAUDE_FOLDER' folder not found"
fi

# Push to origin
log_message "Pushing to origin..."
push_output=$(git push origin main 2>&1)
push_exit_code=$?

if [ $push_exit_code -eq 0 ]; then
    log_message "Push successful: $push_output"
else
    log_message "ERROR during push: $push_output"
    # Try to pull and push again
    log_message "Attempting to pull and push again..."
    git pull origin main --no-edit 2>&1 | tee -a "$LOG_PATH"

    retry_push=$(git push origin main 2>&1)
    retry_exit_code=$?

    if [ $retry_exit_code -eq 0 ]; then
        log_message "Retry push successful"
    else
        log_message "ERROR: Retry push failed: $retry_push"
        exit 1
    fi
fi

log_message "=== Sync completed successfully ==="
