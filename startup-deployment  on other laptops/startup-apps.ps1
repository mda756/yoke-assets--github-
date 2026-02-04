# Startup script to launch GitHub Desktop, Tailscale, and Claude Code
# Created for auto-start on login
# Self-contained - no external file dependencies

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

# Launch Claude Code in a terminal
# Add npm to PATH so Claude command works
$npmPath = "$env:APPDATA\npm"
$env:PATH = "$npmPath;$env:PATH"

# Check if Claude is installed
$claudeInstalled = $false
try {
    $null = Get-Command claude -ErrorAction Stop
    $claudeInstalled = $true
} catch {
    $claudeInstalled = $false
}

if ($claudeInstalled) {
    # Find a suitable working directory
    $workingDir = $env:USERPROFILE

    $candidatePaths = @(
        "$env:USERPROFILE\Dropbox\Yoke Digital\yoke-assets--github-",
        "$env:USERPROFILE\Dropbox\yoke-assets--github-",
        "$env:USERPROFILE\Documents\GitHub\yoke-assets--github-",
        "D:\Dropbox\Yoke Digital\yoke-assets--github-"
    )

    foreach ($path in $candidatePaths) {
        if (Test-Path $path) {
            $workingDir = $path
            break
        }
    }

    # Check if Windows Terminal is available
    $useWindowsTerminal = $false
    try {
        $null = Get-Command wt -ErrorAction Stop
        $useWindowsTerminal = $true
    } catch {
        $useWindowsTerminal = $false
    }

    # Launch Claude in terminal
    if ($useWindowsTerminal) {
        Start-Process wt -ArgumentList "powershell.exe", "-NoExit", "-Command", "cd '$workingDir'; claude"
    } else {
        Start-Process powershell.exe -ArgumentList "-NoExit", "-Command", "cd '$workingDir'; claude"
    }
} else {
    # Claude not installed, just open PowerShell in home directory
    Start-Process powershell.exe -ArgumentList "-NoExit", "-Command", "cd ~; Write-Host 'Claude Code is not installed. Run: npm install -g @anthropic-ai/claude-code' -ForegroundColor Yellow"
}
