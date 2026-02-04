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

# Launch a new PowerShell window
Start-Process powershell.exe
