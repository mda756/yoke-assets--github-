# ============================================================================
# STEP 1: Generate Tailscale Auth Key
# ============================================================================
# Run this ONCE on your main PC to generate a reusable auth key
# ============================================================================

Write-Host "============================================" -ForegroundColor Cyan
Write-Host "  TAILSCALE AUTH KEY GENERATOR" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "Generating a reusable Tailscale auth key..." -ForegroundColor Green
Write-Host ""

# Try to generate auth key via Tailscale CLI
try {
    Write-Host "Attempting to generate auth key..." -ForegroundColor Yellow
    $authKey = & tailscale up --authkey 2>&1

    if ($authKey -match "tskey-") {
        Write-Host "✓ Auth key generated successfully!" -ForegroundColor Green
        Write-Host ""
        Write-Host "Your auth key:" -ForegroundColor Cyan
        Write-Host $authKey -ForegroundColor Yellow
        Write-Host ""
        Write-Host "This key has been saved to: auth-key.txt" -ForegroundColor Gray
        $authKey | Out-File -FilePath "$PSScriptRoot\auth-key.txt" -Encoding UTF8
    } else {
        throw "CLI method failed"
    }
} catch {
    # Manual method
    Write-Host "⚠ Automatic generation not available" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Please generate an auth key manually:" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "1. Opening Tailscale Admin Console..." -ForegroundColor Yellow
    Start-Process "https://login.tailscale.com/admin/settings/keys"
    Write-Host ""
    Write-Host "2. Click 'Generate auth key'" -ForegroundColor Yellow
    Write-Host "3. Settings:" -ForegroundColor Yellow
    Write-Host "   - Description: 'Laptop Deployment Key'" -ForegroundColor Gray
    Write-Host "   - Reusable: YES (check this box!)" -ForegroundColor Gray
    Write-Host "   - Ephemeral: NO" -ForegroundColor Gray
    Write-Host "   - Preauthorized: YES (recommended)" -ForegroundColor Gray
    Write-Host ""
    Write-Host "4. Copy the generated key (starts with 'tskey-')" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "5. Paste it here: " -ForegroundColor Cyan -NoNewline
    $manualKey = Read-Host

    if ($manualKey -match "tskey-") {
        Write-Host ""
        Write-Host "✓ Auth key saved!" -ForegroundColor Green
        $manualKey | Out-File -FilePath "$PSScriptRoot\auth-key.txt" -Encoding UTF8
        Write-Host "Saved to: auth-key.txt" -ForegroundColor Gray
    } else {
        Write-Host ""
        Write-Host "✗ Invalid key format" -ForegroundColor Red
    }
}

Write-Host ""
Write-Host "Next step: Edit DEPLOY-COMPLETE-SETUP.ps1" -ForegroundColor Cyan
Write-Host "and paste this auth key into the configuration section" -ForegroundColor Cyan
Write-Host ""
Write-Host "Press any key to exit..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
