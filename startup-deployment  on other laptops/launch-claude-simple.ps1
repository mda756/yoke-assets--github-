# Launch Claude Code in the GitHub repository folder

# Set the GitHub repository path
$githubFolder = "C:\Users\matth\Dropbox\Yoke Digital\yoke-assets--github-"

# Change to GitHub folder (or home if it doesn't exist)
if (Test-Path $githubFolder) {
    Set-Location $githubFolder
    Write-Host "Opening Claude in: $githubFolder" -ForegroundColor Green
} else {
    Set-Location ~
    Write-Host "GitHub folder not found, opening in home directory" -ForegroundColor Yellow
}

# Add npm to PATH so Claude command works
$npmPath = "$env:APPDATA\npm"
$env:PATH = "$npmPath;$env:PATH"

# Launch Claude
Write-Host "Starting Claude Code..." -ForegroundColor Cyan
Start-Sleep -Milliseconds 500
claude
