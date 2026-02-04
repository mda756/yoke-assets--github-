@echo off
REM Simple launcher for Claude Code in PowerShell
REM This gets called by startup-apps.ps1

REM Set the full path to Claude (npm global bin)
set CLAUDE_PATH=%APPDATA%\npm\claude.cmd

REM Check if Windows Terminal is installed
where wt >nul 2>&1
if %errorlevel% equ 0 (
    REM Use Windows Terminal with PowerShell
    start "" wt.exe -p "Windows PowerShell" powershell.exe -NoExit -Command "Set-Location ~; & '%CLAUDE_PATH%'"
) else (
    REM Use regular PowerShell
    start "" powershell.exe -NoExit -Command "Set-Location ~; & '%CLAUDE_PATH%'"
)
