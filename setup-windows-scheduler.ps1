# Setup Windows Task Scheduler for Git Auto-Sync
# Run this script as Administrator

$taskName = "GitAutoSync-YokeAssets"
$scriptPath = "C:\Users\matth\Dropbox\Yoke Digital\yoke-assets--github-\sync-repo.ps1"
$workingDirectory = "C:\Users\matth\Dropbox\Yoke Digital\yoke-assets--github-"

# Check if running as Administrator
$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)

if (-not $isAdmin) {
    Write-Host "ERROR: This script must be run as Administrator" -ForegroundColor Red
    Write-Host "Right-click PowerShell and select 'Run as Administrator', then run this script again." -ForegroundColor Yellow
    exit 1
}

# Delete existing task if it exists
$existingTask = Get-ScheduledTask -TaskName $taskName -ErrorAction SilentlyContinue
if ($existingTask) {
    Write-Host "Removing existing task..." -ForegroundColor Yellow
    Unregister-ScheduledTask -TaskName $taskName -Confirm:$false
}

# Create action
$action = New-ScheduledTaskAction `
    -Execute "powershell.exe" `
    -Argument "-NoProfile -WindowStyle Hidden -ExecutionPolicy Bypass -File `"$scriptPath`"" `
    -WorkingDirectory $workingDirectory

# Create trigger (every 15 minutes)
$trigger = New-ScheduledTaskTrigger -Once -At (Get-Date) -RepetitionInterval (New-TimeSpan -Minutes 15) -RepetitionDuration ([TimeSpan]::MaxValue)

# Create settings
$settings = New-ScheduledTaskSettingsSet `
    -AllowStartIfOnBatteries `
    -DontStopIfGoingOnBatteries `
    -StartWhenAvailable `
    -RunOnlyIfNetworkAvailable `
    -DontStopOnIdleEnd `
    -ExecutionTimeLimit (New-TimeSpan -Minutes 10)

# Create principal (run as current user)
$principal = New-ScheduledTaskPrincipal `
    -UserId $env:USERNAME `
    -LogonType S4U `
    -RunLevel Highest

# Register the task
Register-ScheduledTask `
    -TaskName $taskName `
    -Action $action `
    -Trigger $trigger `
    -Settings $settings `
    -Principal $principal `
    -Description "Automatically syncs the yoke-assets repository every 15 minutes"

Write-Host "`nTask '$taskName' created successfully!" -ForegroundColor Green
Write-Host "The sync script will run every 15 minutes." -ForegroundColor Cyan
Write-Host "`nYou can manage this task in Task Scheduler:" -ForegroundColor Yellow
Write-Host "  - Search for 'Task Scheduler' in Windows" -ForegroundColor Gray
Write-Host "  - Look for '$taskName' in the task list" -ForegroundColor Gray
Write-Host "`nTo test the task immediately, run:" -ForegroundColor Yellow
Write-Host "  Start-ScheduledTask -TaskName '$taskName'" -ForegroundColor Gray
