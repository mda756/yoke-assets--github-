@echo off
REM Simple launcher for Claude Code
REM Calls the PowerShell script that launches Claude

REM Get the directory where this batch file is located
set SCRIPT_DIR=%~dp0

REM Check if Windows Terminal is installed
where wt >nul 2>&1
if %errorlevel% equ 0 (
    REM Use Windows Terminal
    start "" wt.exe -p "Windows PowerShell" powershell.exe -NoExit -ExecutionPolicy Bypass -File "%SCRIPT_DIR%launch-claude-simple.ps1"
) else (
    REM Use regular PowerShell
    start "" powershell.exe -NoExit -ExecutionPolicy Bypass -File "%SCRIPT_DIR%launch-claude-simple.ps1"
)
