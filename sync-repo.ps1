# Git Auto-Sync Script for Windows
# Logs activity and handles conflicts gracefully

$repoPath = "C:\Users\matth\Dropbox\Yoke Digital\yoke-assets--github-"
$logPath = "C:\Users\matth\Dropbox\Yoke Digital\yoke-assets--github-\sync-log.txt"
$claudeFolder = "claude code creator"

function Write-Log {
    param([string]$message)
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $logMessage = "[$timestamp] $message"
    Write-Host $logMessage
    Add-Content -Path $logPath -Value $logMessage
}

function Handle-MergeConflict {
    Write-Log "Merge conflict detected. Attempting to resolve..."

    # Abort the current merge
    git merge --abort 2>&1 | Out-Null

    # Stash local changes
    Write-Log "Stashing local changes..."
    git stash push -m "Auto-stash before sync - $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')"

    # Pull again
    Write-Log "Pulling from origin after stash..."
    git pull origin main

    # Try to apply stash
    Write-Log "Attempting to re-apply stashed changes..."
    $stashResult = git stash pop 2>&1

    if ($LASTEXITCODE -ne 0) {
        Write-Log "Could not automatically re-apply changes. Changes are saved in stash."
        Write-Log "Manual intervention may be required."
        return $false
    }

    return $true
}

try {
    Set-Location -Path $repoPath
    Write-Log "=== Starting sync process ==="

    # Check if we're in a git repository
    $isRepo = git rev-parse --git-dir 2>&1
    if ($LASTEXITCODE -ne 0) {
        Write-Log "ERROR: Not a git repository"
        exit 1
    }

    # Fetch latest changes
    Write-Log "Fetching from origin..."
    git fetch origin 2>&1 | Out-Null

    # Pull changes from origin
    Write-Log "Pulling changes from origin..."
    $pullOutput = git pull origin main 2>&1

    if ($LASTEXITCODE -ne 0 -and $pullOutput -match "CONFLICT") {
        if (-not (Handle-MergeConflict)) {
            Write-Log "Failed to handle merge conflict automatically"
            exit 1
        }
    } elseif ($LASTEXITCODE -ne 0) {
        Write-Log "ERROR during pull: $pullOutput"
        exit 1
    } else {
        Write-Log "Pull successful: $pullOutput"
    }

    # Check for changes in claude code creator folder
    $claudeFolderPath = Join-Path -Path $repoPath -ChildPath $claudeFolder

    if (Test-Path $claudeFolderPath) {
        Write-Log "Checking for changes in '$claudeFolder' folder..."

        # Add all changes in claude code creator folder
        git add "$claudeFolder/*" 2>&1 | Out-Null

        # Check if there are staged changes
        $status = git status --porcelain
        $stagedChanges = $status | Where-Object { $_ -match "^[AM]" }

        if ($stagedChanges) {
            Write-Log "Found changes in '$claudeFolder'. Committing..."

            # Create commit message
            $commitMessage = "Auto-sync: Updates to claude code creator folder - $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')"

            git commit -m $commitMessage

            if ($LASTEXITCODE -eq 0) {
                Write-Log "Commit successful"
            } else {
                Write-Log "ERROR: Commit failed"
                exit 1
            }
        } else {
            Write-Log "No changes to commit in '$claudeFolder'"
        }
    } else {
        Write-Log "WARNING: '$claudeFolder' folder not found"
    }

    # Push to origin
    Write-Log "Pushing to origin..."
    $pushOutput = git push origin main 2>&1

    if ($LASTEXITCODE -eq 0) {
        Write-Log "Push successful: $pushOutput"
    } else {
        Write-Log "ERROR during push: $pushOutput"
        # Try to pull and push again
        Write-Log "Attempting to pull and push again..."
        git pull origin main --no-edit 2>&1 | Out-Null
        $retryPush = git push origin main 2>&1

        if ($LASTEXITCODE -eq 0) {
            Write-Log "Retry push successful"
        } else {
            Write-Log "ERROR: Retry push failed: $retryPush"
            exit 1
        }
    }

    Write-Log "=== Sync completed successfully ==="

} catch {
    Write-Log "ERROR: Exception occurred - $($_.Exception.Message)"
    exit 1
}
