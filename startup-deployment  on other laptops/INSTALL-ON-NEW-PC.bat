@echo off
REM ============================================================================
REM SUPER SIMPLE LAUNCHER - Just double-click this file!
REM ============================================================================

echo.
echo ════════════════════════════════════════════
echo   PC SETUP - AUTOMATIC INSTALLER
echo ════════════════════════════════════════════
echo.
echo This will install:
echo   - Tailscale
echo   - GitHub Desktop
echo   - Git configuration
echo   - Auto-startup launcher
echo.
echo Press Ctrl+C to cancel, or
pause

REM Request administrator privileges
net session >nul 2>&1
if %errorLevel% == 0 (
    echo Running with administrator privileges...
    powershell.exe -ExecutionPolicy Bypass -File "%~dp0AUTO-SETUP-WITH-PROMPTS.ps1"
) else (
    echo Requesting administrator privileges...
    powershell.exe -Command "Start-Process powershell -Verb RunAs -ArgumentList '-ExecutionPolicy Bypass -File ""%~dp0AUTO-SETUP-WITH-PROMPTS.ps1""'"
)
