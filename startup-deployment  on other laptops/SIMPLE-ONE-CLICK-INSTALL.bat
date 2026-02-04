@echo off
REM ============================================================================
REM ONE-CLICK INSTALLER - Just double-click this file!
REM ============================================================================
REM This stays open so you can see what's happening!
REM ============================================================================

mode con: cols=80 lines=30
color 0A
title PC Setup - One Click Installer

REM Store the script directory (with trailing backslash)
set "SCRIPT_DIR=%~dp0"

echo.
echo ========================================================================
echo                    SIMPLE ONE-CLICK PC SETUP
echo ========================================================================
echo.
echo  This will:
echo    - Check what's already installed
echo    - Install missing software (Tailscale, GitHub Desktop, Node.js, Claude)
echo    - Configure Git
echo    - Setup auto-startup
echo.
echo  Window will stay open so you can see progress!
echo.
echo ========================================================================
echo.
timeout /t 3 /nobreak >nul

echo Checking for administrator rights...
echo.

net session >nul 2>&1
if %errorLevel% == 0 (
    echo [OK] Running as Administrator
    echo.
    echo Starting installation...
    echo.
    timeout /t 2 /nobreak >nul
    powershell.exe -ExecutionPolicy Bypass -NoExit -File "%SCRIPT_DIR%ONE-CLICK-SETUP.ps1"
) else (
    echo [NOTICE] Need administrator rights to install software
    echo.
    echo Requesting admin access... ^(click YES when Windows asks^)
    echo.
    timeout /t 3 /nobreak >nul

    REM Launch PowerShell script directly with admin - simpler approach
    powershell.exe -Command "Start-Process powershell.exe -Verb RunAs -ArgumentList '-ExecutionPolicy Bypass -NoExit -File \"%SCRIPT_DIR%ONE-CLICK-SETUP.ps1\"'"

    echo.
    echo A new admin window should have opened.
    echo If nothing happened, right-click this file and select "Run as administrator"
    echo.
    pause
)
