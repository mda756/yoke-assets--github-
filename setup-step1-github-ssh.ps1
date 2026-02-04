# Step 1: GitHub SSH Key Setup
# This script helps you add your SSH key to GitHub

$publicKeyPath = "$env:USERPROFILE\.ssh\id_ed25519.pub"

Write-Host "=== GitHub SSH Key Setup ===" -ForegroundColor Cyan
Write-Host ""

# Check if key exists
if (Test-Path $publicKeyPath) {
    $publicKey = Get-Content $publicKeyPath

    Write-Host "Your SSH public key:" -ForegroundColor Yellow
    Write-Host $publicKey -ForegroundColor Green
    Write-Host ""

    # Copy to clipboard
    $publicKey | Set-Clipboard
    Write-Host "The key has been copied to your clipboard!" -ForegroundColor Green
    Write-Host ""

    Write-Host "Next steps:" -ForegroundColor Yellow
    Write-Host "1. Go to: https://github.com/settings/keys" -ForegroundColor White
    Write-Host "2. Click 'New SSH key'" -ForegroundColor White
    Write-Host "3. Title: 'Windows PC - Yoke Digital'" -ForegroundColor White
    Write-Host "4. Paste the key (already in clipboard)" -ForegroundColor White
    Write-Host "5. Click 'Add SSH key'" -ForegroundColor White
    Write-Host ""

    Write-Host "Press any key after you've added the key to GitHub..." -ForegroundColor Cyan
    $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")

    Write-Host ""
    Write-Host "Testing SSH connection to GitHub..." -ForegroundColor Cyan

    # Test SSH connection
    $sshTest = ssh -T git@github.com 2>&1

    if ($sshTest -match "successfully authenticated") {
        Write-Host "SUCCESS! SSH connection to GitHub is working!" -ForegroundColor Green
        Write-Host ""
        Write-Host "Now run: .\setup-step2-commit-changes.ps1" -ForegroundColor Yellow
    } else {
        Write-Host "SSH test output: $sshTest" -ForegroundColor Yellow
        Write-Host ""
        Write-Host "If you see 'Permission denied', make sure you added the key to GitHub." -ForegroundColor Red
        Write-Host "Then run this script again to test." -ForegroundColor Yellow
    }

} else {
    Write-Host "ERROR: SSH key not found at $publicKeyPath" -ForegroundColor Red
    Write-Host "The key should have been created automatically." -ForegroundColor Yellow
    Write-Host "You may need to generate it manually with:" -ForegroundColor Yellow
    Write-Host "ssh-keygen -t ed25519 -C `"tech@yokedigital.com`"" -ForegroundColor Gray
}
