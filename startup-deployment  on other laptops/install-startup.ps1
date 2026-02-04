# Deployment script - Run this on each PC to install startup apps
# Right-click and select "Run with PowerShell"

Write-Host "Installing startup apps launcher..." -ForegroundColor Green

$startupFolder = [Environment]::GetFolderPath('Startup')
$scriptPath = Join-Path $PSScriptRoot "startup-apps.ps1"
$vbsPath = Join-Path $PSScriptRoot "startup-apps.vbs"

# Copy files to Startup folder
Copy-Item $scriptPath $startupFolder -Force
Copy-Item $vbsPath $startupFolder -Force

Write-Host "`nStartup apps installed successfully!" -ForegroundColor Green
Write-Host "Location: $startupFolder" -ForegroundColor Cyan
Write-Host "`nThe following will auto-start on next login:" -ForegroundColor Yellow
Write-Host "  - GitHub Desktop"
Write-Host "  - Tailscale"
Write-Host "  - PowerShell window"
Write-Host "`nPress any key to exit..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
