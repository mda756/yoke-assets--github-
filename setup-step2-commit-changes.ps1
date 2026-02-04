# Step 2: Commit Existing Changes
# This script handles all the untracked files before setting up auto-sync

$repoPath = "C:\Users\matth\Dropbox\Yoke Digital\yoke-assets--github-"

Write-Host "=== Commit Existing Changes ===" -ForegroundColor Cyan
Write-Host ""

Set-Location -Path $repoPath

Write-Host "Current repository status:" -ForegroundColor Yellow
git status --short

Write-Host ""
Write-Host "This will commit ALL untracked files and changes." -ForegroundColor Yellow
Write-Host "Files that should be committed:" -ForegroundColor Cyan
Write-Host "  - claude code creator folder (all files)" -ForegroundColor White
Write-Host "  - DEBUG folder" -ForegroundColor White
Write-Host "  - build visuals with claude code folder" -ForegroundColor White
Write-Host "  - chatgpt instructions folder" -ForegroundColor White
Write-Host "  - trump-statement-analysis folder" -ForegroundColor White
Write-Host "  - trump-trading-system folder" -ForegroundColor White
Write-Host "  - Modified files" -ForegroundColor White
Write-Host ""

Write-Host "Do you want to proceed? (y/n): " -ForegroundColor Yellow -NoNewline
$response = Read-Host

if ($response -ne "y" -and $response -ne "Y") {
    Write-Host "Setup cancelled." -ForegroundColor Red
    exit
}

Write-Host ""
Write-Host "Pulling latest changes from origin first..." -ForegroundColor Cyan
git pull origin main --no-edit

Write-Host ""
Write-Host "Adding all files..." -ForegroundColor Cyan
git add .

Write-Host ""
Write-Host "Creating commit..." -ForegroundColor Cyan
$commitMessage = "Add all project files before setting up auto-sync system"
git commit -m $commitMessage

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "Commit created successfully!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Pushing to GitHub..." -ForegroundColor Cyan
    git push origin main

    if ($LASTEXITCODE -eq 0) {
        Write-Host ""
        Write-Host "SUCCESS! All changes have been pushed to GitHub!" -ForegroundColor Green
        Write-Host ""
        Write-Host "Next step: Set up Task Scheduler" -ForegroundColor Yellow
        Write-Host "Run PowerShell as Administrator and execute:" -ForegroundColor Yellow
        Write-Host "  cd `"$repoPath`"" -ForegroundColor Gray
        Write-Host "  .\setup-windows-scheduler.ps1" -ForegroundColor Gray
    } else {
        Write-Host ""
        Write-Host "ERROR: Failed to push to GitHub" -ForegroundColor Red
        Write-Host "You may need to pull and merge first, then try again" -ForegroundColor Yellow
    }
} else {
    Write-Host ""
    Write-Host "No changes to commit, or commit failed" -ForegroundColor Yellow
    Write-Host "Check git status for more information" -ForegroundColor Gray
}
