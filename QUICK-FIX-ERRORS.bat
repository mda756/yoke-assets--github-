@echo off
REM ============================================================================
REM QUICK FIX FOR FILE TRANSFER ERRORS
REM ============================================================================
REM This closes unnecessary browser tabs and clears temp files
REM ============================================================================

color 0A
title Quick Fix for File Transfer Errors

echo.
echo ========================================================================
echo             QUICK FIX FOR FILE TRANSFER ERRORS
echo ========================================================================
echo.
echo This will:
echo   1. Show current browser tab counts
echo   2. Offer to close browsers (optional)
echo   3. Clear temp files
echo   4. Restart Dropbox
echo.
echo ========================================================================
echo.

REM Count browser instances
echo Checking browser instances...
echo.

for /f %%a in ('tasklist ^| find /c "chrome.exe"') do set CHROME_COUNT=%%a
for /f %%a in ('tasklist ^| find /c "msedge.exe"') do set EDGE_COUNT=%%a

echo   Chrome instances: %CHROME_COUNT%
echo   Edge instances: %EDGE_COUNT%
echo.

if %CHROME_COUNT% GTR 20 (
    echo   [WARNING] Chrome has many tabs open ^(%CHROME_COUNT%^)
    echo   This can cause file transfer errors!
    echo.
)

if %EDGE_COUNT% GTR 20 (
    echo   [WARNING] Edge has many tabs open ^(%EDGE_COUNT%^)
    echo   This can cause file transfer errors!
    echo.
)

echo ========================================================================
echo.
echo Do you want to close all browsers? ^(Save your work first!^)
echo.
set /p CLOSE_BROWSERS="Close browsers? (Y/N): "

if /i "%CLOSE_BROWSERS%"=="Y" (
    echo.
    echo Closing browsers...
    taskkill /F /IM chrome.exe 2>nul
    taskkill /F /IM msedge.exe 2>nul
    taskkill /F /IM firefox.exe 2>nul
    echo   [OK] Browsers closed
    timeout /t 2 /nobreak >nul
)

echo.
echo Cleaning temp files...
del /q /f "%TEMP%\*" 2>nul
echo   [OK] Temp files cleared
timeout /t 2 /nobreak >nul

echo.
echo Restarting Dropbox...
taskkill /F /IM Dropbox.exe 2>nul
timeout /t 3 /nobreak >nul
start "" "%APPDATA%\Dropbox\bin\Dropbox.exe"
echo   [OK] Dropbox restarted
timeout /t 2 /nobreak >nul

echo.
echo ========================================================================
echo                        FIX COMPLETE!
echo ========================================================================
echo.
echo What was done:
if /i "%CLOSE_BROWSERS%"=="Y" (
    echo   [OK] Browsers closed
)
echo   [OK] Temp files cleared
echo   [OK] Dropbox restarted
echo.
echo You should see fewer "Unable to transfer files" errors now!
echo.
echo ========================================================================
echo.
pause
