# Launch Claude Code in the GitHub repository folder
# Works on any user account - auto-detects paths

# Try to find a suitable working directory (in priority order)
$workingDir = $null

# 1. Check for Dropbox yoke-assets folder (any user)
$dropboxPaths = @(
    "$env:USERPROFILE\Dropbox\Yoke Digital\yoke-assets--github-",
    "$env:USERPROFILE\Dropbox\yoke-assets--github-",
    "D:\Dropbox\Yoke Digital\yoke-assets--github-"
)

foreach ($path in $dropboxPaths) {
    if (Test-Path $path) {
        $workingDir = $path
        break
    }
}

# 2. Check for GitHub Desktop default clone location
if (-not $workingDir) {
    $githubDesktopPath = "$env:USERPROFILE\Documents\GitHub\yoke-assets--github-"
    if (Test-Path $githubDesktopPath) {
        $workingDir = $githubDesktopPath
    }
}

# 3. Check common dev folders
if (-not $workingDir) {
    $devPaths = @(
        "$env:USERPROFILE\repos\yoke-assets--github-",
        "$env:USERPROFILE\code\yoke-assets--github-",
        "$env:USERPROFILE\projects\yoke-assets--github-"
    )
    foreach ($path in $devPaths) {
        if (Test-Path $path) {
            $workingDir = $path
            break
        }
    }
}

# 4. Fall back to home directory
if (-not $workingDir) {
    $workingDir = $env:USERPROFILE
}

# Change to working directory
Set-Location $workingDir
Write-Host "Opening Claude in: $workingDir" -ForegroundColor Green

# Add npm to PATH so Claude command works
$npmPath = "$env:APPDATA\npm"
if ($env:PATH -notlike "*$npmPath*") {
    $env:PATH = "$npmPath;$env:PATH"
}

# Launch Claude
Write-Host "Starting Claude Code..." -ForegroundColor Cyan
Start-Sleep -Milliseconds 500
claude
