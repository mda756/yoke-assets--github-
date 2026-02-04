# ============================================================================
# File Transfer Error Diagnostic Tool
# ============================================================================
# Run this to check what might be causing "Unable to transfer files" errors
# ============================================================================

Write-Host ""
Write-Host "========================================================================" -ForegroundColor Cyan
Write-Host "           FILE TRANSFER ERROR DIAGNOSTIC TOOL" -ForegroundColor Cyan
Write-Host "========================================================================" -ForegroundColor Cyan
Write-Host ""

# Check 1: Dropbox Status
Write-Host "[1] Checking Dropbox Status..." -ForegroundColor Yellow
$dropboxProcess = Get-Process -Name "Dropbox" -ErrorAction SilentlyContinue
if ($dropboxProcess) {
    Write-Host "   [OK] Dropbox is running" -ForegroundColor Green
    Write-Host "   Process Count: $($dropboxProcess.Count)" -ForegroundColor Gray
} else {
    Write-Host "   [WARNING] Dropbox is not running" -ForegroundColor Red
}

# Check 2: File System Access
Write-Host ""
Write-Host "[2] Checking Dropbox Folder Access..." -ForegroundColor Yellow
$dropboxPaths = @(
    "C:\Users\matth\Dropbox",
    "C:\Users\matth\Dropbox\Yoke Digital",
    "C:\Users\matth\Dropbox\Yoke Digital\yoke-assets--github-"
)

foreach ($path in $dropboxPaths) {
    if (Test-Path $path) {
        try {
            $testFile = Join-Path $path "test_write_$(Get-Date -Format 'yyyyMMdd_HHmmss').tmp"
            "test" | Out-File $testFile -ErrorAction Stop
            Remove-Item $testFile -ErrorAction Stop
            Write-Host "   [OK] Can write to: $path" -ForegroundColor Green
        } catch {
            Write-Host "   [ERROR] Cannot write to: $path" -ForegroundColor Red
            Write-Host "          Error: $($_.Exception.Message)" -ForegroundColor Red
        }
    } else {
        Write-Host "   [ERROR] Path not found: $path" -ForegroundColor Red
    }
}

# Check 3: Startup Scripts
Write-Host ""
Write-Host "[3] Checking Startup Scripts..." -ForegroundColor Yellow
$startupFolder = [Environment]::GetFolderPath('Startup')
$startupFiles = Get-ChildItem $startupFolder | Where-Object { $_.Extension -in @('.vbs', '.ps1', '.bat') }
if ($startupFiles) {
    Write-Host "   Found $($startupFiles.Count) startup scripts:" -ForegroundColor Cyan
    foreach ($file in $startupFiles) {
        Write-Host "   - $($file.Name)" -ForegroundColor Gray
    }
} else {
    Write-Host "   [OK] No custom startup scripts" -ForegroundColor Green
}

# Check 4: Running Python Scripts
Write-Host ""
Write-Host "[4] Checking for Running Python Scripts..." -ForegroundColor Yellow
$pythonProcesses = Get-Process -Name "python*" -ErrorAction SilentlyContinue
if ($pythonProcesses) {
    Write-Host "   [FOUND] Python processes running:" -ForegroundColor Yellow
    foreach ($proc in $pythonProcesses) {
        Write-Host "   - $($proc.Name) (PID: $($proc.Id))" -ForegroundColor Gray
    }
} else {
    Write-Host "   [OK] No Python processes running" -ForegroundColor Green
}

# Check 5: Browser Processes
Write-Host ""
Write-Host "[5] Checking Browser Processes..." -ForegroundColor Yellow
$browsers = @("chrome", "msedge", "firefox", "brave")
$browserCount = 0
foreach ($browser in $browsers) {
    $proc = Get-Process -Name $browser -ErrorAction SilentlyContinue
    if ($proc) {
        Write-Host "   [FOUND] $browser ($($proc.Count) instances)" -ForegroundColor Cyan
        $browserCount += $proc.Count
    }
}
if ($browserCount -eq 0) {
    Write-Host "   [OK] No browsers running" -ForegroundColor Green
}

# Check 6: Recent DEBUG Folder Activity
Write-Host ""
Write-Host "[6] Checking DEBUG Folder for Recent Errors..." -ForegroundColor Yellow
$debugFolder = "C:\Users\matth\Dropbox\Yoke Digital\yoke-assets--github-\DEBUG"
if (Test-Path $debugFolder) {
    $recentFiles = Get-ChildItem $debugFolder -File | Where-Object { $_.LastWriteTime -gt (Get-Date).AddHours(-24) } | Sort-Object LastWriteTime -Descending
    if ($recentFiles) {
        Write-Host "   [FOUND] $($recentFiles.Count) error screenshots in last 24 hours:" -ForegroundColor Yellow
        $recentFiles | Select-Object -First 5 | ForEach-Object {
            Write-Host "   - $($_.Name) at $($_.LastWriteTime)" -ForegroundColor Gray
        }
        if ($recentFiles.Count -gt 5) {
            Write-Host "   ... and $($recentFiles.Count - 5) more" -ForegroundColor Gray
        }
    } else {
        Write-Host "   [OK] No recent error screenshots" -ForegroundColor Green
    }
} else {
    Write-Host "   [INFO] DEBUG folder not found" -ForegroundColor Gray
}

# Check 7: Disk Space
Write-Host ""
Write-Host "[7] Checking Disk Space..." -ForegroundColor Yellow
$drive = Get-PSDrive C
$freeGB = [math]::Round($drive.Free / 1GB, 2)
$totalGB = [math]::Round(($drive.Free + $drive.Used) / 1GB, 2)
$percentFree = [math]::Round(($drive.Free / ($drive.Free + $drive.Used)) * 100, 1)

if ($percentFree -lt 10) {
    Write-Host "   [WARNING] Low disk space: $freeGB GB free ($percentFree% free)" -ForegroundColor Red
} elseif ($percentFree -lt 20) {
    Write-Host "   [WARNING] Disk space getting low: $freeGB GB free ($percentFree% free)" -ForegroundColor Yellow
} else {
    Write-Host "   [OK] Disk space: $freeGB GB free of $totalGB GB ($percentFree% free)" -ForegroundColor Green
}

# Recommendations
Write-Host ""
Write-Host "========================================================================" -ForegroundColor Cyan
Write-Host "                         RECOMMENDATIONS" -ForegroundColor Cyan
Write-Host "========================================================================" -ForegroundColor Cyan
Write-Host ""

if ($dropboxProcess -and $startupFiles) {
    Write-Host "ISSUE: Startup scripts run while Dropbox is syncing" -ForegroundColor Yellow
    Write-Host "FIX: The sort-dropbox-folders.vbs has been updated with delays" -ForegroundColor Green
    Write-Host ""
}

if ($recentFiles.Count -gt 10) {
    Write-Host "ISSUE: Multiple file transfer errors detected ($($recentFiles.Count) in 24h)" -ForegroundColor Yellow
    Write-Host "POSSIBLE CAUSES:" -ForegroundColor Cyan
    Write-Host "  1. Browser file uploads timing out" -ForegroundColor White
    Write-Host "  2. Dropbox sync conflicts" -ForegroundColor White
    Write-Host "  3. Antivirus blocking file operations" -ForegroundColor White
    Write-Host "  4. Network connectivity issues" -ForegroundColor White
    Write-Host ""
    Write-Host "SUGGESTED FIXES:" -ForegroundColor Cyan
    Write-Host "  1. Restart your computer to clear any locked processes" -ForegroundColor White
    Write-Host "  2. Pause Dropbox sync before large file uploads" -ForegroundColor White
    Write-Host "  3. Check antivirus settings (add exclusions if needed)" -ForegroundColor White
    Write-Host "  4. Close unnecessary browser tabs before file uploads" -ForegroundColor White
    Write-Host ""
}

Write-Host "========================================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Press any key to exit..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
