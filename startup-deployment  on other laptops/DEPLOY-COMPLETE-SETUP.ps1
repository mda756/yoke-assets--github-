# ============================================================================
# COMPLETE PC SETUP SCRIPT - ONE-CLICK DEPLOYMENT
# ============================================================================
# This script will:
# 1. Install Tailscale
# 2. Install GitHub Desktop
# 3. Configure Git
# 4. Install GitHub CLI
# 5. Set up auto-startup launcher (GitHub → Tailscale → Terminal)
# 6. Configure Claude Code settings (auto-approval for routine operations)
# ============================================================================

# Requires Administrator privileges
if (-NOT ([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")) {
    Write-Host "This script needs Administrator privileges!" -ForegroundColor Red
    Write-Host "Right-click this script and select 'Run as Administrator'" -ForegroundColor Yellow
    pause
    exit
}

Write-Host "============================================" -ForegroundColor Cyan
Write-Host "  COMPLETE PC SETUP - AUTO INSTALLER" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""

# ============================================================================
# CONFIGURATION - Edit these values if needed
# ============================================================================
$TAILSCALE_AUTH_KEY = "PASTE_YOUR_TAILSCALE_AUTH_KEY_HERE"
$GIT_USERNAME = "mda756"
$GIT_EMAIL = "matt@Yokehealth.com"

# ============================================================================
# 1. INSTALL WINGET (if not present)
# ============================================================================
Write-Host "[1/6] Checking for winget..." -ForegroundColor Green
try {
    $wingetVersion = winget --version
    Write-Host "  ✓ Winget already installed: $wingetVersion" -ForegroundColor Gray
} catch {
    Write-Host "  Installing winget (App Installer)..." -ForegroundColor Yellow
    Add-AppxPackage -RegisterByFamilyName -MainPackage Microsoft.DesktopAppInstaller_8wekyb3d8bbwe
}

# ============================================================================
# 2. INSTALL TAILSCALE
# ============================================================================
Write-Host ""
Write-Host "[2/6] Installing Tailscale..." -ForegroundColor Green

if (Test-Path "C:\Program Files\Tailscale\tailscale.exe") {
    Write-Host "  ✓ Tailscale already installed" -ForegroundColor Gray
} else {
    Write-Host "  Downloading and installing Tailscale..." -ForegroundColor Yellow
    winget install --id tailscale.tailscale --silent --accept-package-agreements --accept-source-agreements
    Start-Sleep -Seconds 5
}

# Connect to Tailscale
Write-Host "  Connecting to Tailscale network..." -ForegroundColor Yellow
if ($TAILSCALE_AUTH_KEY -ne "PASTE_YOUR_TAILSCALE_AUTH_KEY_HERE") {
    & "C:\Program Files\Tailscale\tailscale.exe" up --authkey=$TAILSCALE_AUTH_KEY --accept-routes
    Write-Host "  ✓ Tailscale connected!" -ForegroundColor Gray
} else {
    Write-Host "  ⚠ No auth key provided - manual login required" -ForegroundColor Yellow
    Write-Host "    Run: tailscale up" -ForegroundColor Yellow
}

# ============================================================================
# 3. INSTALL GITHUB DESKTOP
# ============================================================================
Write-Host ""
Write-Host "[3/6] Installing GitHub Desktop..." -ForegroundColor Green

if (Test-Path "$env:LOCALAPPDATA\GitHubDesktop\GitHubDesktop.exe") {
    Write-Host "  ✓ GitHub Desktop already installed" -ForegroundColor Gray
} else {
    Write-Host "  Downloading and installing GitHub Desktop..." -ForegroundColor Yellow
    winget install --id GitHub.GitHubDesktop --silent --accept-package-agreements --accept-source-agreements
}

# ============================================================================
# 4. CONFIGURE GIT
# ============================================================================
Write-Host ""
Write-Host "[4/6] Configuring Git..." -ForegroundColor Green

git config --global user.name "$GIT_USERNAME"
git config --global user.email "$GIT_EMAIL"
git config --global credential.helper manager
git config --global credential.https://dev.azure.com.usehttppath true

Write-Host "  ✓ Git configured:" -ForegroundColor Gray
Write-Host "    Name: $GIT_USERNAME" -ForegroundColor Gray
Write-Host "    Email: $GIT_EMAIL" -ForegroundColor Gray

# ============================================================================
# 5. INSTALL GITHUB CLI (for easier authentication)
# ============================================================================
Write-Host ""
Write-Host "[5/6] Installing GitHub CLI..." -ForegroundColor Green

try {
    $ghVersion = gh --version
    Write-Host "  ✓ GitHub CLI already installed" -ForegroundColor Gray
} catch {
    Write-Host "  Installing GitHub CLI..." -ForegroundColor Yellow
    winget install --id GitHub.cli --silent --accept-package-agreements --accept-source-agreements
}

# ============================================================================
# 6. SETUP STARTUP LAUNCHER
# ============================================================================
Write-Host ""
Write-Host "[6/6] Setting up startup launcher..." -ForegroundColor Green

$startupFolder = [Environment]::GetFolderPath('Startup')
$scriptPath = Join-Path $PSScriptRoot "startup-apps.ps1"
$vbsPath = Join-Path $PSScriptRoot "startup-apps.vbs"

if (Test-Path $scriptPath) {
    Copy-Item $scriptPath $startupFolder -Force
    Copy-Item $vbsPath $startupFolder -Force
    Write-Host "  ✓ Startup launcher installed" -ForegroundColor Gray
} else {
    Write-Host "  ⚠ Startup files not found in deployment folder" -ForegroundColor Yellow
}

# ============================================================================
# 7. CONFIGURE CLAUDE CODE SETTINGS (AUTO-APPROVAL)
# ============================================================================
Write-Host ""
Write-Host "[7/7] Configuring Claude Code settings..." -ForegroundColor Green

$claudeSettingsDir = Join-Path $env:USERPROFILE ".claude"
$claudeSettingsFile = Join-Path $claudeSettingsDir "settings.local.json"
$settingsTemplate = Join-Path $PSScriptRoot "claude-settings-template.json"

# Create .claude directory if it doesn't exist
if (-not (Test-Path $claudeSettingsDir)) {
    New-Item -ItemType Directory -Path $claudeSettingsDir -Force | Out-Null
    Write-Host "  ✓ Created .claude directory" -ForegroundColor Gray
}

# Copy settings template if it exists
if (Test-Path $settingsTemplate) {
    Copy-Item $settingsTemplate $claudeSettingsFile -Force
    Write-Host "  ✓ Claude settings configured for auto-approval" -ForegroundColor Gray
    Write-Host "    (Routine operations auto-approved, security/stability prompts remain)" -ForegroundColor Gray
} else {
    Write-Host "  ⚠ Settings template not found - manual configuration needed" -ForegroundColor Yellow
}

# ============================================================================
# COMPLETION
# ============================================================================
Write-Host ""
Write-Host "============================================" -ForegroundColor Green
Write-Host "  INSTALLATION COMPLETE!" -ForegroundColor Green
Write-Host "============================================" -ForegroundColor Green
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host ""
Write-Host "1. GitHub Authentication:" -ForegroundColor Yellow
Write-Host "   - Open GitHub Desktop (it will auto-start on next login)"
Write-Host "   - Sign in with your GitHub account"
Write-Host "   OR run: gh auth login" -ForegroundColor Gray
Write-Host ""
Write-Host "2. Tailscale (if not connected):" -ForegroundColor Yellow
Write-Host "   - Click the Tailscale tray icon and sign in"
Write-Host "   OR generate an auth key at: https://login.tailscale.com/admin/settings/keys"
Write-Host ""
Write-Host "3. On next login, these will auto-start IN ORDER:" -ForegroundColor Yellow
Write-Host "   ✓ GitHub Desktop (starts first)"
Write-Host "   ✓ Tailscale (waits 3 seconds)"
Write-Host "   ✓ Windows Terminal (waits 5 seconds)"
Write-Host "   → Sequential startup ensures everything initializes properly"
Write-Host ""
Write-Host "4. Claude Code configured for auto-approval:" -ForegroundColor Yellow
Write-Host "   ✓ Routine operations proceed automatically"
Write-Host "   ⚠ Security/stability operations still prompt"
Write-Host "   → No more pressing '2' for regular tasks!"
Write-Host ""
Write-Host "Press any key to exit..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
