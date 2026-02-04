# Simple PowerShell script to launch Claude Code
# No complex quoting or escaping needed

# Set location to home directory
Set-Location ~

# Get the path to Claude
$claudePath = "$env:APPDATA\npm\claude.cmd"

# Check if it exists
if (Test-Path $claudePath) {
    # Run Claude
    & $claudePath
} else {
    Write-Host "ERROR: Claude not found at: $claudePath" -ForegroundColor Red
    Write-Host ""
    Write-Host "Please install Claude Code:" -ForegroundColor Yellow
    Write-Host "  npm install -g @anthropic-ai/claude-code" -ForegroundColor White
    Write-Host ""
    pause
}
