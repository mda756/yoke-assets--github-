# Startup script to launch GitHub Desktop, Tailscale, and PowerShell
# Created for auto-start on login

# Launch GitHub Desktop (common installation paths)
$githubPaths = @(
    "$env:LOCALAPPDATA\GitHubDesktop\GitHubDesktop.exe",
    "$env:LOCALAPPDATA\Programs\GitHubDesktop\GitHubDesktop.exe",
    "C:\Program Files\GitHubDesktop\GitHubDesktop.exe"
)

foreach ($path in $githubPaths) {
    if (Test-Path $path) {
        Start-Process $path
        break
    }
}

# Launch Tailscale (start the GUI)
$tailscalePaths = @(
    "C:\Program Files\Tailscale\tailscale-ipn.exe",
    "C:\Program Files\Tailscale\tailscale.exe"
)

foreach ($path in $tailscalePaths) {
    if (Test-Path $path) {
        Start-Process $path
        break
    }
}

# Launch PowerShell with Claude Code
# First check if claude is installed
$claudeInstalled = $false
try {
    $null = Get-Command claude -ErrorAction Stop
    $claudeInstalled = $true
} catch {
    $claudeInstalled = $false
}

if ($claudeInstalled) {
    # Launch Windows Terminal (or PowerShell) with Claude Code
    # Check if Windows Terminal is available
    $wtInstalled = Get-Command wt -ErrorAction SilentlyContinue

    if ($wtInstalled) {
        # Use Windows Terminal with Claude Code
        Start-Process wt -ArgumentList "powershell.exe -NoExit -Command `"cd '$HOME'; claude`""
    } else {
        # Use regular PowerShell with Claude Code
        Start-Process powershell.exe -ArgumentList "-NoExit -Command `"cd '$HOME'; claude`""
    }
} else {
    # Claude not installed, just open PowerShell
    Start-Process powershell.exe
}
