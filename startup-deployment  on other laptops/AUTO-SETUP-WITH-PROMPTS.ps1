# ============================================================================
# AUTOMATIC PC SETUP - WITH INTERACTIVE PROMPTS
# ============================================================================
# Alternative version that prompts for auth key during installation
# Use this if you don't want to pre-configure the auth key
# ============================================================================

# Check for Administrator privileges
if (-NOT ([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")) {
    Write-Host "═══════════════════════════════════════" -ForegroundColor Red
    Write-Host "  ADMINISTRATOR PRIVILEGES REQUIRED" -ForegroundColor Red
    Write-Host "═══════════════════════════════════════" -ForegroundColor Red
    Write-Host ""
    Write-Host "Please:" -ForegroundColor Yellow
    Write-Host "1. Right-click this script" -ForegroundColor Yellow
    Write-Host "2. Select 'Run as Administrator'" -ForegroundColor Yellow
    Write-Host ""
    pause
    exit
}

Clear-Host
Write-Host "╔════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║  COMPLETE PC SETUP - AUTO INSTALLER  ║" -ForegroundColor Cyan
Write-Host "╚════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""

# Configuration
$GIT_USERNAME = "mda756"
$GIT_EMAIL = "matt@Yokehealth.com"

# Check for auth key file
$authKeyFile = Join-Path $PSScriptRoot "auth-key.txt"
if (Test-Path $authKeyFile) {
    $TAILSCALE_AUTH_KEY = (Get-Content $authKeyFile -Raw).Trim()
    Write-Host "✓ Found Tailscale auth key in auth-key.txt" -ForegroundColor Green
    Write-Host ""
} else {
    Write-Host "Tailscale Auth Key Setup" -ForegroundColor Yellow
    Write-Host "════════════════════════" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "I need a Tailscale auth key to connect this PC automatically." -ForegroundColor White
    Write-Host ""
    Write-Host "Options:" -ForegroundColor Cyan
    Write-Host "  1. Paste an existing auth key now" -ForegroundColor White
    Write-Host "  2. Open browser to generate one" -ForegroundColor White
    Write-Host "  3. Skip Tailscale auto-connect (manual login later)" -ForegroundColor White
    Write-Host ""
    $choice = Read-Host "Enter choice (1/2/3)"

    switch ($choice) {
        "1" {
            Write-Host ""
            Write-Host "Paste your Tailscale auth key (starts with 'tskey-'): " -ForegroundColor Cyan -NoNewline
            $TAILSCALE_AUTH_KEY = Read-Host
        }
        "2" {
            Write-Host ""
            Write-Host "Opening Tailscale admin panel..." -ForegroundColor Yellow
            Start-Process "https://login.tailscale.com/admin/settings/keys"
            Write-Host ""
            Write-Host "In the browser:" -ForegroundColor Cyan
            Write-Host "  1. Click 'Generate auth key'" -ForegroundColor White
            Write-Host "  2. Check 'Reusable' and 'Preauthorized'" -ForegroundColor White
            Write-Host "  3. Click 'Generate key'" -ForegroundColor White
            Write-Host "  4. Copy the key" -ForegroundColor White
            Write-Host ""
            Write-Host "Paste the auth key here: " -ForegroundColor Cyan -NoNewline
            $TAILSCALE_AUTH_KEY = Read-Host
        }
        "3" {
            $TAILSCALE_AUTH_KEY = ""
            Write-Host ""
            Write-Host "⚠ Skipping auto-connect. You'll need to sign in manually." -ForegroundColor Yellow
        }
    }
    Write-Host ""
}

Write-Host "Starting installation..." -ForegroundColor Green
Write-Host ""
Start-Sleep -Seconds 2

# ============================================================================
# Install Winget
# ============================================================================
Write-Host "[1/6] Checking for winget..." -ForegroundColor Cyan
try {
    $null = winget --version
    Write-Host "      ✓ Winget found" -ForegroundColor Green
} catch {
    Write-Host "      Installing winget..." -ForegroundColor Yellow
    Add-AppxPackage -RegisterByFamilyName -MainPackage Microsoft.DesktopAppInstaller_8wekyb3d8bbwe
}

# ============================================================================
# Install Tailscale
# ============================================================================
Write-Host ""
Write-Host "[2/6] Installing Tailscale..." -ForegroundColor Cyan

if (Test-Path "C:\Program Files\Tailscale\tailscale.exe") {
    Write-Host "      ✓ Already installed" -ForegroundColor Green
} else {
    Write-Host "      Installing (this may take 1-2 minutes)..." -ForegroundColor Yellow
    winget install --id tailscale.tailscale --silent --accept-package-agreements --accept-source-agreements | Out-Null
    Start-Sleep -Seconds 5
    Write-Host "      ✓ Installed" -ForegroundColor Green
}

if ($TAILSCALE_AUTH_KEY -match "tskey-") {
    Write-Host "      Connecting to Tailscale network..." -ForegroundColor Yellow
    & "C:\Program Files\Tailscale\tailscale.exe" up --authkey=$TAILSCALE_AUTH_KEY --accept-routes 2>&1 | Out-Null
    Write-Host "      ✓ Connected to Tailscale!" -ForegroundColor Green
}

# ============================================================================
# Install GitHub Desktop
# ============================================================================
Write-Host ""
Write-Host "[3/6] Installing GitHub Desktop..." -ForegroundColor Cyan

if (Test-Path "$env:LOCALAPPDATA\GitHubDesktop\GitHubDesktop.exe") {
    Write-Host "      ✓ Already installed" -ForegroundColor Green
} else {
    Write-Host "      Installing (this may take 2-3 minutes)..." -ForegroundColor Yellow
    winget install --id GitHub.GitHubDesktop --silent --accept-package-agreements --accept-source-agreements | Out-Null
    Write-Host "      ✓ Installed" -ForegroundColor Green
}

# ============================================================================
# Configure Git
# ============================================================================
Write-Host ""
Write-Host "[4/6] Configuring Git..." -ForegroundColor Cyan

git config --global user.name "$GIT_USERNAME" 2>&1 | Out-Null
git config --global user.email "$GIT_EMAIL" 2>&1 | Out-Null
git config --global credential.helper manager 2>&1 | Out-Null
git config --global credential.https://dev.azure.com.usehttppath true 2>&1 | Out-Null

Write-Host "      ✓ Configured ($GIT_USERNAME / $GIT_EMAIL)" -ForegroundColor Green

# ============================================================================
# Install GitHub CLI
# ============================================================================
Write-Host ""
Write-Host "[5/6] Installing GitHub CLI..." -ForegroundColor Cyan

try {
    $null = gh --version 2>&1
    Write-Host "      ✓ Already installed" -ForegroundColor Green
} catch {
    Write-Host "      Installing..." -ForegroundColor Yellow
    winget install --id GitHub.cli --silent --accept-package-agreements --accept-source-agreements | Out-Null
    Write-Host "      ✓ Installed" -ForegroundColor Green
}

# ============================================================================
# Setup Startup Launcher
# ============================================================================
Write-Host ""
Write-Host "[6/6] Setting up startup launcher..." -ForegroundColor Cyan

$startupFolder = [Environment]::GetFolderPath('Startup')
$scriptPath = Join-Path $PSScriptRoot "startup-apps.ps1"
$vbsPath = Join-Path $PSScriptRoot "startup-apps.vbs"

if (Test-Path $scriptPath) {
    Copy-Item $scriptPath $startupFolder -Force
    Copy-Item $vbsPath $startupFolder -Force
    Write-Host "      ✓ Startup launcher configured" -ForegroundColor Green
}

# ============================================================================
# Completion
# ============================================================================
Write-Host ""
Write-Host "╔════════════════════════════════════════╗" -ForegroundColor Green
Write-Host "║     INSTALLATION COMPLETE! ✓         ║" -ForegroundColor Green
Write-Host "╚════════════════════════════════════════╝" -ForegroundColor Green
Write-Host ""

Write-Host "What's installed:" -ForegroundColor Cyan
Write-Host "  ✓ Tailscale (VPN)" -ForegroundColor White
Write-Host "  ✓ GitHub Desktop" -ForegroundColor White
Write-Host "  ✓ GitHub CLI" -ForegroundColor White
Write-Host "  ✓ Git (configured)" -ForegroundColor White
Write-Host "  ✓ Auto-startup launcher" -ForegroundColor White
Write-Host ""

Write-Host "On next login, these will auto-start:" -ForegroundColor Cyan
Write-Host "  • GitHub Desktop" -ForegroundColor White
Write-Host "  • Tailscale" -ForegroundColor White
Write-Host "  • PowerShell window" -ForegroundColor White
Write-Host ""

Write-Host "First-time setup:" -ForegroundColor Yellow
Write-Host "  → GitHub Desktop will ask you to sign in (one-time)" -ForegroundColor White
if (-not ($TAILSCALE_AUTH_KEY -match "tskey-")) {
    Write-Host "  → Tailscale: Click tray icon and sign in (one-time)" -ForegroundColor White
}
Write-Host ""

Write-Host "Restart your PC to activate auto-startup" -ForegroundColor Cyan
Write-Host ""
Write-Host "Press any key to exit..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
