# Git Auto-Sync Master Setup Script
# This script guides you through the complete setup process

$repoPath = "C:\Users\matth\Dropbox\Yoke Digital\yoke-assets--github-"

function Show-Header {
    param([string]$text)
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host $text -ForegroundColor Cyan
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host ""
}

function Show-Step {
    param([string]$number, [string]$title)
    Write-Host ""
    Write-Host "STEP ${number}: $title" -ForegroundColor Yellow
    Write-Host ("=" * 50) -ForegroundColor Gray
    Write-Host ""
}

Set-Location -Path $repoPath

Show-Header "GIT AUTO-SYNC SETUP WIZARD"

Write-Host "This wizard will help you set up automated git syncing between:" -ForegroundColor White
Write-Host "  - Your Windows PC" -ForegroundColor Green
Write-Host "  - Your DigitalOcean Droplet (134.209.186.176)" -ForegroundColor Green
Write-Host "  - GitHub repository" -ForegroundColor Green
Write-Host ""
Write-Host "The system will sync every 15 minutes automatically." -ForegroundColor White
Write-Host ""
Write-Host "Prerequisites:" -ForegroundColor Yellow
Write-Host "  [x] SSH key generated" -ForegroundColor Green
Write-Host "  [x] Git remote updated to use SSH" -ForegroundColor Green
Write-Host ""

Write-Host "Press any key to continue..." -ForegroundColor Cyan
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")

# ============================================================
# STEP 1: GitHub SSH Setup
# ============================================================
Show-Step "1" "Add SSH Key to GitHub"

$publicKeyPath = "$env:USERPROFILE\.ssh\id_ed25519.pub"
$publicKey = Get-Content $publicKeyPath

Write-Host "Your SSH public key:" -ForegroundColor Yellow
Write-Host $publicKey -ForegroundColor Green
Write-Host ""

$publicKey | Set-Clipboard
Write-Host "The key has been COPIED TO CLIPBOARD!" -ForegroundColor Green
Write-Host ""

Write-Host "ACTION REQUIRED:" -ForegroundColor Red
Write-Host "1. Open: https://github.com/settings/keys" -ForegroundColor White
Write-Host "2. Click 'New SSH key'" -ForegroundColor White
Write-Host "3. Title: Windows PC - Yoke Digital" -ForegroundColor White
Write-Host "4. Paste the key (Ctrl+V)" -ForegroundColor White
Write-Host "5. Click 'Add SSH key'" -ForegroundColor White
Write-Host ""

Write-Host "Press any key AFTER you've added the key to GitHub..." -ForegroundColor Cyan
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")

Write-Host ""
Write-Host "Testing SSH connection to GitHub..." -ForegroundColor Cyan
$sshTest = ssh -T git@github.com 2>&1

if ($sshTest -match "successfully authenticated") {
    Write-Host "SUCCESS! GitHub SSH is working!" -ForegroundColor Green
} else {
    Write-Host "WARNING: SSH test result: $sshTest" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "If you see 'Permission denied', go back and add the key to GitHub." -ForegroundColor Red
    Write-Host "Do you want to continue anyway? (y/n): " -ForegroundColor Yellow -NoNewline
    $response = Read-Host
    if ($response -ne "y" -and $response -ne "Y") {
        Write-Host "Setup cancelled. Run this script again when ready." -ForegroundColor Red
        exit
    }
}

# ============================================================
# STEP 2: Commit Existing Changes
# ============================================================
Show-Step "2" "Commit Existing Changes"

Write-Host "Before setting up auto-sync, we need to commit existing changes." -ForegroundColor White
Write-Host ""
Write-Host "Current status:" -ForegroundColor Yellow
git status --short | Select-Object -First 20
Write-Host "... (showing first 20 items)" -ForegroundColor Gray
Write-Host ""

Write-Host "This will:" -ForegroundColor Yellow
Write-Host "  1. Pull latest changes from GitHub" -ForegroundColor White
Write-Host "  2. Add ALL untracked files and changes" -ForegroundColor White
Write-Host "  3. Create a commit" -ForegroundColor White
Write-Host "  4. Push to GitHub" -ForegroundColor White
Write-Host ""

Write-Host "Do you want to proceed? (y/n): " -ForegroundColor Yellow -NoNewline
$response = Read-Host

if ($response -ne "y" -and $response -ne "Y") {
    Write-Host "Setup cancelled." -ForegroundColor Red
    exit
}

Write-Host ""
Write-Host "Pulling from origin..." -ForegroundColor Cyan
git pull origin main --no-edit

Write-Host ""
Write-Host "Adding all files..." -ForegroundColor Cyan
git add .

Write-Host ""
Write-Host "Creating commit..." -ForegroundColor Cyan
git commit -m "Add all project files before setting up auto-sync system"

Write-Host ""
Write-Host "Pushing to GitHub..." -ForegroundColor Cyan
git push origin main

if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "ERROR: Failed to push to GitHub" -ForegroundColor Red
    Write-Host "Please resolve any issues and run this script again" -ForegroundColor Yellow
    exit
}

Write-Host ""
Write-Host "SUCCESS! All changes committed and pushed!" -ForegroundColor Green

# ============================================================
# STEP 3: Test Sync Script
# ============================================================
Show-Step "3" "Test Sync Script"

Write-Host "Testing the sync script..." -ForegroundColor Cyan
Write-Host ""

.\sync-repo.ps1

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "SUCCESS! Sync script works!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Log file location:" -ForegroundColor Yellow
    Write-Host "  $repoPath\sync-log.txt" -ForegroundColor Gray
    Write-Host ""
    Write-Host "Last 10 log lines:" -ForegroundColor Yellow
    Get-Content "$repoPath\sync-log.txt" -Tail 10
} else {
    Write-Host ""
    Write-Host "ERROR: Sync script failed" -ForegroundColor Red
    Write-Host "Check the log file for details" -ForegroundColor Yellow
    exit
}

# ============================================================
# STEP 4: Setup Task Scheduler
# ============================================================
Show-Step "4" "Setup Task Scheduler"

Write-Host "Now we need to set up Windows Task Scheduler." -ForegroundColor White
Write-Host "This requires ADMINISTRATOR privileges." -ForegroundColor Yellow
Write-Host ""

$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)

if (-not $isAdmin) {
    Write-Host "ACTION REQUIRED:" -ForegroundColor Red
    Write-Host "1. Close this window" -ForegroundColor White
    Write-Host "2. Right-click PowerShell" -ForegroundColor White
    Write-Host "3. Select 'Run as Administrator'" -ForegroundColor White
    Write-Host "4. Run this command:" -ForegroundColor White
    Write-Host "   cd `"$repoPath`"" -ForegroundColor Gray
    Write-Host "   .\setup-windows-scheduler.ps1" -ForegroundColor Gray
    Write-Host ""
    Write-Host "Press any key to exit..." -ForegroundColor Cyan
    $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
    exit
}

Write-Host "Running as Administrator - proceeding with Task Scheduler setup..." -ForegroundColor Green
Write-Host ""

.\setup-windows-scheduler.ps1

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "SUCCESS! Task Scheduler configured!" -ForegroundColor Green
}

# ============================================================
# STEP 5: Droplet Setup Instructions
# ============================================================
Show-Step "5" "Droplet Setup"

Write-Host "Windows setup is complete!" -ForegroundColor Green
Write-Host ""
Write-Host "Now you need to set up the droplet." -ForegroundColor Yellow
Write-Host ""
Write-Host "Open a NEW PowerShell window and run these commands:" -ForegroundColor White
Write-Host ""
Write-Host "# Connect to droplet" -ForegroundColor Gray
Write-Host "ssh root@134.209.186.176" -ForegroundColor Cyan
Write-Host "# Password: Digitalocan 2025Rootpassword75X" -ForegroundColor Gray
Write-Host ""
Write-Host "# Generate SSH key on droplet" -ForegroundColor Gray
Write-Host "ssh-keygen -t ed25519 -C `"tech@yokedigital.com`" -f ~/.ssh/id_ed25519 -N `"`"" -ForegroundColor Cyan
Write-Host "cat ~/.ssh/id_ed25519.pub" -ForegroundColor Cyan
Write-Host ""
Write-Host "# Add that key to GitHub (Settings > SSH keys)" -ForegroundColor Gray
Write-Host "# Then test the connection:" -ForegroundColor Gray
Write-Host "ssh -T git@github.com" -ForegroundColor Cyan
Write-Host ""
Write-Host "# Clone or update repository" -ForegroundColor Gray
Write-Host "cd /root" -ForegroundColor Cyan
Write-Host "git clone git@github.com:mda756/yoke-assets--github-.git" -ForegroundColor Cyan
Write-Host "cd yoke-assets--github-" -ForegroundColor Cyan
Write-Host "git config user.name `"techyokedigital`"" -ForegroundColor Cyan
Write-Host "git config user.email `"tech@yokedigital.com`"" -ForegroundColor Cyan
Write-Host ""
Write-Host "# Run the setup script" -ForegroundColor Gray
Write-Host "chmod +x setup-droplet-cron.sh" -ForegroundColor Cyan
Write-Host "./setup-droplet-cron.sh" -ForegroundColor Cyan
Write-Host ""
Write-Host ""

Write-Host "For detailed instructions, see:" -ForegroundColor Yellow
Write-Host "  $repoPath\SYNC_SETUP_INSTRUCTIONS.md" -ForegroundColor Gray
Write-Host ""

Show-Header "WINDOWS SETUP COMPLETE!"

Write-Host "Your Windows PC is now set up for auto-sync!" -ForegroundColor Green
Write-Host ""
Write-Host "The sync will run automatically every 15 minutes." -ForegroundColor White
Write-Host ""
Write-Host "To monitor activity:" -ForegroundColor Yellow
Write-Host "  Get-Content `"$repoPath\sync-log.txt`" -Tail 20 -Wait" -ForegroundColor Gray
Write-Host ""
Write-Host "To manually trigger sync:" -ForegroundColor Yellow
Write-Host "  Start-ScheduledTask -TaskName 'GitAutoSync-YokeAssets'" -ForegroundColor Gray
Write-Host ""
Write-Host "Complete the droplet setup using the commands above." -ForegroundColor Yellow
