@echo off
REM ============================================================================
REM ONE-CLICK INSTALLER - Just double-click this file!
REM ============================================================================
REM This stays open so you can see what's happening!
REM ============================================================================

mode con: cols=80 lines=30
color 0A
title PC Setup - One Click Installer

echo.
echo ========================================================================
echo                    SIMPLE ONE-CLICK PC SETUP
echo ========================================================================
echo.
echo  This will:
echo    - Check what's already installed
echo    - Install missing software (Tailscale, GitHub Desktop)
echo    - Configure Git
echo    - Setup auto-startup
echo.
echo  Window will stay open so you can see progress!
echo.
echo ========================================================================
echo.
timeout /t 3 /nobreak

echo Checking for administrator rights...
echo.

net session >nul 2>&1
if %errorLevel% == 0 (
    echo [OK] Running as Administrator
    echo.
    echo Starting installation...
    echo.
    timeout /t 2 /nobreak
    powershell.exe -ExecutionPolicy Bypass -NoExit -File "%~dp0ONE-CLICK-SETUP.ps1"
) else (
    echo [NOTICE] Need administrator rights to install software
    echo.
    echo Requesting admin access... ^(click YES when Windows asks^)
    echo.
    timeout /t 3 /nobreak

    REM Launch with admin and keep window open
    powershell.exe -Command "Start-Process cmd -Verb RunAs -ArgumentList '/k cd /d ""%~dp0"" && powershell.exe -ExecutionPolicy Bypass -NoExit -File ""%~dp0ONE-CLICK-SETUP.ps1""'"

    echo.
    echo If nothing happened, the request was cancelled.
    echo Try running this file again and click YES when prompted.
    echo.
    pause
)
