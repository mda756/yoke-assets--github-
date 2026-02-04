STARTUP APPS AUTO-LAUNCHER
===========================

This package will auto-start the following programs when you log in:
- GitHub Desktop
- Tailscale
- New PowerShell window

INSTALLATION ON THIS PC:
Already installed! It will run on your next login.

INSTALLATION ON OTHER PCs:
1. Copy this entire "startup-deployment" folder to the other PC
2. Right-click "install-startup.ps1" and select "Run with PowerShell"
3. Done! Programs will auto-start on next login

ALTERNATIVE METHOD (Manual):
1. Press Win+R and type: shell:startup
2. Copy "startup-apps.ps1" and "startup-apps.vbs" to that folder
3. Done!

TO TEST WITHOUT RESTARTING:
- Double-click "startup-apps.vbs" to test the launcher

TO REMOVE:
1. Press Win+R and type: shell:startup
2. Delete "startup-apps.ps1" and "startup-apps.vbs"

NOTES:
- The VBS file runs the script silently (no console window flash)
- If GitHub Desktop path is different, edit startup-apps.ps1
- Works on Windows 10/11
