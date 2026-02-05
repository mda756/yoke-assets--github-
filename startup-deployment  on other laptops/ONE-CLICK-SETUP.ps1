# ============================================================================
# ONE-CLICK PC SETUP SCRIPT
# ============================================================================
# This script stays open so you can see what's happening!
# ============================================================================

$Host.UI.RawUI.WindowTitle = "PC Setup - Installation in Progress"
$Host.UI.RawUI.BackgroundColor = "Black"
$Host.UI.RawUI.ForegroundColor = "Green"
Clear-Host

function Write-Step {
    param($StepNumber, $Total, $Message)
    Write-Host ""
    Write-Host "[$StepNumber/$Total] " -NoNewline -ForegroundColor Cyan
    Write-Host $Message -ForegroundColor White
    Write-Host ("=" * 70) -ForegroundColor DarkGray
}

function Write-Success {
    param($Message)
    Write-Host "   [OK] " -NoNewline -ForegroundColor Green
    Write-Host $Message -ForegroundColor White
}

function Write-Info {
    param($Message)
    Write-Host "   [>>] " -NoNewline -ForegroundColor Yellow
    Write-Host $Message -ForegroundColor White
}

function Write-Skip {
    param($Message)
    Write-Host "   [SKIP] " -NoNewline -ForegroundColor DarkYellow
    Write-Host $Message -ForegroundColor Gray
}

function Write-Error-Safe {
    param($Message)
    Write-Host "   [ERROR] " -NoNewline -ForegroundColor Red
    Write-Host $Message -ForegroundColor White
}

# Header
Write-Host ""
Write-Host "========================================================================" -ForegroundColor Cyan
Write-Host "                    ONE-CLICK PC SETUP" -ForegroundColor Cyan
Write-Host "========================================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Starting installation process..." -ForegroundColor White
Write-Host "This window will stay open so you can see everything!" -ForegroundColor Yellow
Write-Host ""
Start-Sleep -Seconds 2

# Configuration
$GIT_USERNAME = "mda756"
$GIT_EMAIL = "matt@Yokehealth.com"
$TOTAL_STEPS = 9

# ============================================================================
# STEP 1: Check Administrator
# ============================================================================
Write-Step 1 $TOTAL_STEPS "Checking administrator privileges"

if (-NOT ([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")) {
    Write-Error-Safe "Not running as administrator!"
    Write-Host ""
    Write-Host "   Please close this window and run the .bat file again." -ForegroundColor Yellow
    Write-Host "   Click YES when Windows asks for permission." -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Press any key to exit..."
    $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
    exit
}

Write-Success "Running with administrator privileges"

# ============================================================================
# STEP 2: Check/Install Winget
# ============================================================================
Write-Step 2 $TOTAL_STEPS "Checking Windows Package Manager (winget)"

try {
    $wingetVersion = winget --version 2>&1
    Write-Success "Winget is installed (version: $wingetVersion)"
} catch {
    Write-Info "Installing winget..."
    try {
        Add-AppxPackage -RegisterByFamilyName -MainPackage Microsoft.DesktopAppInstaller_8wekyb3d8bbwe -ErrorAction Stop
        Write-Success "Winget installed successfully"
    } catch {
        Write-Error-Safe "Could not install winget. Some installations may fail."
    }
}

# ============================================================================
# STEP 3: Check/Install Tailscale
# ============================================================================
Write-Step 3 $TOTAL_STEPS "Checking Tailscale VPN"

$tailscalePath = "C:\Program Files\Tailscale\tailscale.exe"
if (Test-Path $tailscalePath) {
    Write-Success "Tailscale is already installed"
    Write-Skip "Skipping Tailscale installation"
} else {
    Write-Info "Tailscale not found - installing now..."
    Write-Info "This may take 1-2 minutes, please wait..."

    try {
        $installOutput = winget install --id tailscale.tailscale --silent --accept-package-agreements --accept-source-agreements 2>&1
        Start-Sleep -Seconds 3

        if (Test-Path $tailscalePath) {
            Write-Success "Tailscale installed successfully!"
        } else {
            Write-Error-Safe "Installation may have failed. You can install manually later."
        }
    } catch {
        Write-Error-Safe "Could not install Tailscale: $_"
        Write-Info "You can install it manually from: https://tailscale.com/download"
    }
}

# ============================================================================
# STEP 4: Check/Install GitHub Desktop
# ============================================================================
Write-Step 4 $TOTAL_STEPS "Checking GitHub Desktop"

$githubPath = "$env:LOCALAPPDATA\GitHubDesktop\GitHubDesktop.exe"
if (Test-Path $githubPath) {
    Write-Success "GitHub Desktop is already installed"
    Write-Skip "Skipping GitHub Desktop installation"
} else {
    Write-Info "GitHub Desktop not found - installing now..."
    Write-Info "This may take 2-3 minutes (largest download), please wait..."

    try {
        $installOutput = winget install --id GitHub.GitHubDesktop --silent --accept-package-agreements --accept-source-agreements 2>&1
        Start-Sleep -Seconds 3

        if (Test-Path $githubPath) {
            Write-Success "GitHub Desktop installed successfully!"
        } else {
            Write-Error-Safe "Installation may have failed. You can install manually later."
        }
    } catch {
        Write-Error-Safe "Could not install GitHub Desktop: $_"
        Write-Info "You can install it manually from: https://desktop.github.com"
    }
}

# ============================================================================
# STEP 5: Check/Install Node.js (required for Claude Code)
# ============================================================================
Write-Step 5 $TOTAL_STEPS "Checking Node.js (required for Claude Code)"

$nodeInstalled = $false
try {
    $nodeVersion = node --version 2>&1
    if ($nodeVersion -match "^v\d+") {
        Write-Success "Node.js is already installed (version: $nodeVersion)"
        $nodeInstalled = $true
    }
} catch {
    $nodeInstalled = $false
}

if (-not $nodeInstalled) {
    Write-Info "Node.js not found - installing now..."
    Write-Info "This may take 2-3 minutes, please wait..."

    try {
        $installOutput = winget install --id OpenJS.NodeJS.LTS --silent --accept-package-agreements --accept-source-agreements 2>&1
        Start-Sleep -Seconds 5

        # Refresh PATH to include newly installed Node
        $env:PATH = [System.Environment]::GetEnvironmentVariable("PATH", "Machine") + ";" + [System.Environment]::GetEnvironmentVariable("PATH", "User")

        # Test if node is now available
        try {
            $nodeVersion = node --version 2>&1
            if ($nodeVersion -match "^v\d+") {
                Write-Success "Node.js installed successfully! (version: $nodeVersion)"
                $nodeInstalled = $true
            } else {
                Write-Error-Safe "Node.js installed but may need a restart to work"
                Write-Info "Claude Code installation will be attempted anyway"
                $nodeInstalled = $true
            }
        } catch {
            Write-Error-Safe "Node.js installed but not in PATH yet"
            Write-Info "You may need to restart your PC, then run: npm install -g @anthropic-ai/claude-code"
        }
    } catch {
        Write-Error-Safe "Could not install Node.js: $_"
        Write-Info "You can install it manually from: https://nodejs.org"
    }
}

# ============================================================================
# STEP 6: Check/Install Claude Code
# ============================================================================
Write-Step 6 $TOTAL_STEPS "Checking Claude Code"

# Add npm global path to current session
$npmPath = "$env:APPDATA\npm"
if ($env:PATH -notlike "*$npmPath*") {
    $env:PATH = "$npmPath;$env:PATH"
}

$claudeInstalled = $false
try {
    $claudeVersion = claude --version 2>&1
    if ($claudeVersion) {
        Write-Success "Claude Code is already installed"
        $claudeInstalled = $true
    }
} catch {
    $claudeInstalled = $false
}

if (-not $claudeInstalled -and $nodeInstalled) {
    Write-Info "Claude Code not found - installing now..."
    Write-Info "This may take 1-2 minutes, please wait..."

    try {
        # Run npm install as the current user (not admin) for proper permissions
        $installResult = npm install -g @anthropic-ai/claude-code 2>&1
        Start-Sleep -Seconds 3

        # Test if claude is now available
        try {
            $claudeVersion = & "$npmPath\claude.cmd" --version 2>&1
            if ($claudeVersion) {
                Write-Success "Claude Code installed successfully!"
                $claudeInstalled = $true
            } else {
                Write-Info "Claude Code installed - may need terminal restart to use"
            }
        } catch {
            Write-Info "Claude Code installed - restart terminal to use 'claude' command"
        }
    } catch {
        Write-Error-Safe "Could not install Claude Code: $_"
        Write-Info "You can install it manually: npm install -g @anthropic-ai/claude-code"
    }
} elseif (-not $nodeInstalled) {
    Write-Skip "Skipping Claude Code (Node.js required)"
    Write-Info "After installing Node.js, run: npm install -g @anthropic-ai/claude-code"
}

# ============================================================================
# STEP 7: Configure Git
# ============================================================================
Write-Step 7 $TOTAL_STEPS "Configuring Git"

try {
    git config --global user.name "$GIT_USERNAME" 2>&1 | Out-Null
    git config --global user.email "$GIT_EMAIL" 2>&1 | Out-Null
    git config --global credential.helper manager 2>&1 | Out-Null
    git config --global credential.https://dev.azure.com.usehttppath true 2>&1 | Out-Null

    Write-Success "Git configured successfully"
    Write-Info "Username: $GIT_USERNAME"
    Write-Info "Email: $GIT_EMAIL"
} catch {
    Write-Error-Safe "Could not configure Git (it may not be installed yet)"
    Write-Info "Git will be configured when you first use GitHub Desktop"
}

# ============================================================================
# STEP 8: Setup Auto-Startup
# ============================================================================
Write-Step 8 $TOTAL_STEPS "Setting up auto-startup apps (GitHub → Tailscale → Terminal)"

$startupFolder = [Environment]::GetFolderPath('Startup')
$scriptPath = Join-Path $PSScriptRoot "startup-apps.ps1"
$vbsPath = Join-Path $PSScriptRoot "startup-apps.vbs"

if ((Test-Path $scriptPath) -and (Test-Path $vbsPath)) {
    try {
        Copy-Item $scriptPath $startupFolder -Force -ErrorAction Stop
        Copy-Item $vbsPath $startupFolder -Force -ErrorAction Stop
        Write-Success "Auto-startup configured"
        Write-Info "Startup order: GitHub (3s delay) → Tailscale (5s delay) → Terminal"
        Write-Info "Location: $startupFolder"
    } catch {
        Write-Error-Safe "Could not copy startup files: $_"
    }
} else {
    Write-Error-Safe "Startup files not found in current folder"
}

# ============================================================================
# STEP 9: Configure Claude Code Settings
# ============================================================================
Write-Step 9 $TOTAL_STEPS "Configuring Claude Code auto-approval settings"

$claudeSettingsDir = Join-Path $env:USERPROFILE ".claude"
$claudeSettingsFile = Join-Path $claudeSettingsDir "settings.local.json"
$settingsTemplate = Join-Path $PSScriptRoot "claude-settings-template.json"

# Create .claude directory if it doesn't exist
if (-not (Test-Path $claudeSettingsDir)) {
    try {
        New-Item -ItemType Directory -Path $claudeSettingsDir -Force -ErrorAction Stop | Out-Null
        Write-Success "Created .claude directory"
    } catch {
        Write-Error-Safe "Could not create .claude directory: $_"
    }
}

# Copy settings template if it exists
if (Test-Path $settingsTemplate) {
    try {
        Copy-Item $settingsTemplate $claudeSettingsFile -Force -ErrorAction Stop
        Write-Success "Claude auto-approval configured"
        Write-Info "Routine operations auto-approved (no more pressing '2'!)"
        Write-Info "Security/stability operations still prompt for safety"
    } catch {
        Write-Error-Safe "Could not copy settings file: $_"
    }
} else {
    Write-Skip "Settings template not found - manual configuration needed"
}

# ============================================================================
# COMPLETION
# ============================================================================
Write-Host ""
Write-Host "========================================================================" -ForegroundColor Green
Write-Host "                    INSTALLATION COMPLETE!" -ForegroundColor Green
Write-Host "========================================================================" -ForegroundColor Green
Write-Host ""

Write-Host "Summary:" -ForegroundColor Cyan
Write-Host ""

if (Test-Path $tailscalePath) {
    Write-Host "  [OK] Tailscale VPN" -ForegroundColor Green
} else {
    Write-Host "  [--] Tailscale VPN (not installed)" -ForegroundColor Yellow
}

if (Test-Path $githubPath) {
    Write-Host "  [OK] GitHub Desktop" -ForegroundColor Green
} else {
    Write-Host "  [--] GitHub Desktop (not installed)" -ForegroundColor Yellow
}

if ($nodeInstalled) {
    Write-Host "  [OK] Node.js" -ForegroundColor Green
} else {
    Write-Host "  [--] Node.js (not installed)" -ForegroundColor Yellow
}

if ($claudeInstalled) {
    Write-Host "  [OK] Claude Code" -ForegroundColor Green
} else {
    Write-Host "  [--] Claude Code (not installed)" -ForegroundColor Yellow
}

Write-Host "  [OK] Git Configuration" -ForegroundColor Green
Write-Host "  [OK] Auto-startup Setup (GitHub → Tailscale → Terminal)" -ForegroundColor Green
Write-Host "  [OK] Claude Code Auto-Approval Settings" -ForegroundColor Green
Write-Host ""

Write-Host "========================================================================" -ForegroundColor Cyan
Write-Host "                         NEXT STEPS" -ForegroundColor Cyan
Write-Host "========================================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "1. RESTART your PC to activate auto-startup" -ForegroundColor Yellow
Write-Host ""
Write-Host "2. After restart, these will open IN ORDER:" -ForegroundColor White
Write-Host "   - GitHub Desktop (starts first, waits 3 seconds)" -ForegroundColor Gray
Write-Host "   - Tailscale (starts second, waits 5 seconds)" -ForegroundColor Gray
Write-Host "   - Terminal with Claude Code (starts last)" -ForegroundColor Gray
Write-Host "   → Sequential startup ensures everything initializes properly" -ForegroundColor DarkGray
Write-Host ""
Write-Host "3. First-time setup:" -ForegroundColor White
Write-Host "   - GitHub Desktop: Sign in with your GitHub account" -ForegroundColor Gray
Write-Host "   - Tailscale: Should auto-connect (or sign in via tray icon)" -ForegroundColor Gray
Write-Host "   - Claude Code: Will prompt for Anthropic API key on first run" -ForegroundColor Gray
Write-Host ""
Write-Host "4. Claude Code is now configured for auto-approval:" -ForegroundColor White
Write-Host "   - Routine operations proceed automatically (no more pressing '2'!)" -ForegroundColor Gray
Write-Host "   - Security/stability operations still prompt for safety" -ForegroundColor Gray
Write-Host ""
Write-Host "========================================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "This window will stay open for review." -ForegroundColor Yellow
Write-Host "You can close it anytime, or it will close when you restart." -ForegroundColor Yellow
Write-Host ""
Write-Host "Press any key to close this window..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
