# Startup script to launch GitHub Desktop, Tailscale, and Claude Code
# Created for auto-start on login
# Self-contained - no external file dependencies
# STARTUP ORDER: GitHub → Tailscale → Windows Terminal (with delays for proper initialization)

# STEP 1: Launch GitHub Desktop (common installation paths)
$githubPaths = @(
    "$env:LOCALAPPDATA\GitHubDesktop\GitHubDesktop.exe",
    "$env:LOCALAPPDATA\Programs\GitHubDesktop\GitHubDesktop.exe",
    "C:\Program Files\GitHubDesktop\GitHubDesktop.exe"
)

foreach ($path in $githubPaths) {
    if (Test-Path $path) {
        Start-Process $path
        Write-Host "Starting GitHub Desktop..." -ForegroundColor Green
        break
    }
}

# Wait for GitHub to initialize
Start-Sleep -Seconds 3

# STEP 2: Launch Tailscale (start the GUI)
$tailscalePaths = @(
    "C:\Program Files\Tailscale\tailscale-ipn.exe",
    "C:\Program Files\Tailscale\tailscale.exe"
)

foreach ($path in $tailscalePaths) {
    if (Test-Path $path) {
        Start-Process $path
        Write-Host "Starting Tailscale..." -ForegroundColor Green
        break
    }
}

# Wait for Tailscale to connect
Start-Sleep -Seconds 5

# STEP 3: Launch Claude Code in Windows Terminal
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

    # Launch Claude in terminal with explicit PATH
    $claudePath = "$env:APPDATA\npm"
    if ($useWindowsTerminal) {
        $wtCommand = "-d `"$workingDir`" powershell.exe -NoExit -Command `"`$env:PATH='$claudePath;'+`$env:PATH; claude --trust`""
        Start-Process wt -ArgumentList $wtCommand
    } else {
        Start-Process powershell.exe -ArgumentList "-NoExit", "-Command", "`$env:PATH='$claudePath;'+`$env:PATH; cd '$workingDir'; claude --trust"
    }
} else {
    # Claude not installed, just open PowerShell in home directory
    Start-Process powershell.exe -ArgumentList "-NoExit", "-Command", "cd ~; Write-Host 'Claude Code is not installed. Run: npm install -g @anthropic-ai/claude-code' -ForegroundColor Yellow"
}
