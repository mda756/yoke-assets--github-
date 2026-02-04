@echo off
echo ========================================================================
echo                    TESTING CLAUDE STARTUP
echo ========================================================================
echo.
echo This will test if Claude launches correctly in PowerShell.
echo A new window should open with Claude Code running.
echo.
pause
echo.
echo Launching...
call "%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup\launch-claude.bat"
echo.
echo Did a PowerShell window open with Claude running?
echo If YES: The startup is fixed!
echo If NO: Check if Claude is installed (run: claude --version)
echo.
pause
