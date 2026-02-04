# Git Auto-Sync System

Automated git synchronization between Windows PC and DigitalOcean Droplet.

## What This Does

- Automatically syncs your repository every 15 minutes
- Commits changes from "claude code creator" folder
- Handles merge conflicts gracefully
- Logs all activity for troubleshooting
- Works without manual intervention

## Quick Start

### On Windows

Run this in PowerShell:

```powershell
cd "C:\Users\matth\Dropbox\Yoke Digital\yoke-assets--github-"
.\SETUP-START-HERE.ps1
```

Follow the wizard. It will:
1. Help you add SSH key to GitHub
2. Commit existing changes
3. Test the sync script
4. Set up Task Scheduler
5. Show you droplet setup commands

### On Droplet

After Windows setup, copy/paste these commands:

```bash
ssh root@134.209.186.176
ssh-keygen -t ed25519 -C "tech@yokedigital.com" -f ~/.ssh/id_ed25519 -N ""
cat ~/.ssh/id_ed25519.pub
# Add this key to GitHub, then continue:
ssh -T git@github.com
cd /root
git clone git@github.com:mda756/yoke-assets--github-.git
cd yoke-assets--github-
git config user.name "techyokedigital"
git config user.email "tech@yokedigital.com"
chmod +x setup-droplet-cron.sh
./setup-droplet-cron.sh
```

## Documentation

- **SETUP-START-HERE.ps1** - Interactive setup wizard (recommended)
- **QUICK_REFERENCE.md** - Common commands and troubleshooting
- **SYNC_SETUP_INSTRUCTIONS.md** - Complete manual setup guide

## Files Created

### Scripts
- `sync-repo.ps1` - Windows sync script
- `sync-repo.sh` - Droplet sync script (Bash)
- `setup-windows-scheduler.ps1` - Task Scheduler setup
- `setup-droplet-cron.sh` - Cron job setup

### Setup Helpers
- `setup-step1-github-ssh.ps1` - Add SSH key to GitHub
- `setup-step2-commit-changes.ps1` - Commit existing files
- `SETUP-START-HERE.ps1` - Master setup wizard

### Documentation
- `SYNC_SETUP_INSTRUCTIONS.md` - Full manual
- `QUICK_REFERENCE.md` - Quick commands
- `GIT-SYNC-README.md` - This file

## Prerequisites (Already Done)

- SSH key generated: `C:\Users\matth\.ssh\id_ed25519`
- Git remote updated to SSH: `git@github.com:mda756/yoke-assets--github-.git`

## What You Need to Do

1. **Add SSH key to GitHub** - The wizard will guide you
2. **Run the setup wizard** - `.\SETUP-START-HERE.ps1`
3. **Set up droplet** - Copy/paste commands shown by wizard

That's it!

## Monitoring

**Windows:**
```powershell
Get-Content "C:\Users\matth\Dropbox\Yoke Digital\yoke-assets--github-\sync-log.txt" -Tail 20 -Wait
```

**Droplet:**
```bash
tail -f /root/yoke-assets-sync.log
```

## Status

- **Windows:**
  - [x] SSH key generated
  - [x] Git remote updated to SSH
  - [x] Sync script created
  - [ ] SSH key added to GitHub (you need to do this)
  - [ ] Task Scheduler configured (run setup wizard)

- **Droplet:**
  - [ ] SSH key generated (follow wizard instructions)
  - [ ] SSH key added to GitHub
  - [ ] Repository cloned
  - [ ] Cron job configured

## Support

If anything doesn't work:
1. Check the logs (both machines)
2. Test SSH: `ssh -T git@github.com`
3. Run sync script manually
4. See QUICK_REFERENCE.md for troubleshooting

## Important Notes

- Only "claude code creator" folder is auto-committed
- Everything else needs manual commits
- Scripts handle merge conflicts automatically
- Logs are kept for debugging
- No manual intervention needed after setup
