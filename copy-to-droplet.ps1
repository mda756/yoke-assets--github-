# Copy setup scripts to droplet
# Run this after Windows setup is complete

$dropletIP = "134.209.186.176"
$dropletUser = "root"
$repoPath = "C:\Users\matth\Dropbox\Yoke Digital\yoke-assets--github-"

Write-Host "=== Copy Scripts to Droplet ===" -ForegroundColor Cyan
Write-Host ""
Write-Host "This will copy the sync scripts to your droplet." -ForegroundColor White
Write-Host ""
Write-Host "Droplet: $dropletIP" -ForegroundColor Yellow
Write-Host "Password: Digitalocan 2025Rootpassword75X" -ForegroundColor Yellow
Write-Host ""
Write-Host "Files to copy:" -ForegroundColor White
Write-Host "  - sync-repo.sh" -ForegroundColor Gray
Write-Host "  - setup-droplet-cron.sh" -ForegroundColor Gray
Write-Host ""

Write-Host "Press any key to continue..." -ForegroundColor Cyan
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")

Write-Host ""
Write-Host "Copying sync-repo.sh..." -ForegroundColor Cyan

scp "$repoPath\sync-repo.sh" "${dropletUser}@${dropletIP}:/root/"

if ($LASTEXITCODE -eq 0) {
    Write-Host "SUCCESS: sync-repo.sh copied" -ForegroundColor Green
} else {
    Write-Host "ERROR: Failed to copy sync-repo.sh" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "Copying setup-droplet-cron.sh..." -ForegroundColor Cyan

scp "$repoPath\setup-droplet-cron.sh" "${dropletUser}@${dropletIP}:/root/"

if ($LASTEXITCODE -eq 0) {
    Write-Host "SUCCESS: setup-droplet-cron.sh copied" -ForegroundColor Green
} else {
    Write-Host "ERROR: Failed to copy setup-droplet-cron.sh" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "All files copied successfully!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "Next steps (on droplet):" -ForegroundColor Yellow
Write-Host ""
Write-Host "1. SSH into droplet:" -ForegroundColor White
Write-Host "   ssh $dropletUser@$dropletIP" -ForegroundColor Gray
Write-Host ""
Write-Host "2. Make scripts executable:" -ForegroundColor White
Write-Host "   chmod +x /root/sync-repo.sh" -ForegroundColor Gray
Write-Host "   chmod +x /root/setup-droplet-cron.sh" -ForegroundColor Gray
Write-Host ""
Write-Host "3. Run setup script:" -ForegroundColor White
Write-Host "   /root/setup-droplet-cron.sh" -ForegroundColor Gray
Write-Host ""

Write-Host "OR use the SETUP-START-HERE.ps1 wizard for full guidance." -ForegroundColor Yellow
