@echo off
echo ================================================================
echo          TESTING CLAUDE LAUNCH IN GITHUB FOLDER
echo ================================================================
echo.
echo This will open PowerShell with Claude Code in your GitHub folder.
echo.
pause

REM Launch PowerShell with the script
powershell.exe -NoExit -ExecutionPolicy Bypass -File "%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup\launch-claude-simple.ps1"
