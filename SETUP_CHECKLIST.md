# Git Auto-Sync Setup Checklist

Use this checklist to track your progress through the setup.

---

## Prerequisites (Already Complete)

- [x] SSH key generated on Windows
- [x] Git remote updated to SSH
- [x] All scripts created
- [x] Documentation written

---

## Your Setup Tasks

### Windows Setup

#### 1. Add SSH Key to GitHub
- [ ] Go to https://github.com/settings/keys
- [ ] Click "New SSH key"
- [ ] Title: `Windows PC - Yoke Digital`
- [ ] Paste key: `ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIPJKr/cQAAeHS1FZLJPkM9GTWQv998dIurG1vFp5vVqR tech@yokedigital.com`
- [ ] Click "Add SSH key"
- [ ] Test: `ssh -T git@github.com` (should succeed)

#### 2. Run Setup Wizard
- [ ] Open PowerShell
- [ ] Navigate to: `cd "C:\Users\matth\Dropbox\Yoke Digital\yoke-assets--github-"`
- [ ] Run: `.\SETUP-START-HERE.ps1`
- [ ] Follow all prompts
- [ ] Verify SSH connection succeeds
- [ ] Confirm commit of existing changes
- [ ] Verify sync script test succeeds

#### 3. Setup Task Scheduler (As Administrator)
- [ ] Close current PowerShell
- [ ] Right-click PowerShell → "Run as Administrator"
- [ ] Navigate to: `cd "C:\Users\matth\Dropbox\Yoke Digital\yoke-assets--github-"`
- [ ] Run: `.\setup-windows-scheduler.ps1`
- [ ] Verify task created successfully
- [ ] Test: `Start-ScheduledTask -TaskName "GitAutoSync-YokeAssets"`
- [ ] Check log: `Get-Content "C:\Users\matth\Dropbox\Yoke Digital\yoke-assets--github-\sync-log.txt" -Tail 20`

### Droplet Setup

#### 4. Connect to Droplet
- [ ] Open new PowerShell or terminal
- [ ] Connect: `ssh root@134.209.186.176`
- [ ] Enter password: `Digitalocan 2025Rootpassword75X`
- [ ] Connection successful

#### 5. Generate SSH Key on Droplet
- [ ] Run: `ssh-keygen -t ed25519 -C "tech@yokedigital.com" -f ~/.ssh/id_ed25519 -N ""`
- [ ] Display key: `cat ~/.ssh/id_ed25519.pub`
- [ ] Copy the key output

#### 6. Add Droplet SSH Key to GitHub
- [ ] Go to https://github.com/settings/keys (on your PC)
- [ ] Click "New SSH key"
- [ ] Title: `DigitalOcean Droplet - Yoke Digital`
- [ ] Paste the droplet's public key
- [ ] Click "Add SSH key"
- [ ] Back on droplet, test: `ssh -T git@github.com` (should succeed)

#### 7. Clone Repository on Droplet
- [ ] Navigate: `cd /root`
- [ ] Clone: `git clone git@github.com:mda756/yoke-assets--github-.git`
- [ ] Navigate: `cd yoke-assets--github-`
- [ ] Configure: `git config user.name "techyokedigital"`
- [ ] Configure: `git config user.email "tech@yokedigital.com"`
- [ ] Verify: `git status` (should work)

#### 8. Setup Cron Job on Droplet
- [ ] Make executable: `chmod +x setup-droplet-cron.sh`
- [ ] Run setup: `./setup-droplet-cron.sh`
- [ ] Verify cron: `crontab -l` (should show sync-repo.sh entry)
- [ ] Test manually: `./sync-repo.sh`
- [ ] Check log: `tail -20 /root/yoke-assets-sync.log`

### Verification

#### 9. Test Windows → Droplet Sync
- [ ] On Windows, create test file:
  ```powershell
  echo "test from windows" > "C:\Users\matth\Dropbox\Yoke Digital\yoke-assets--github-\claude code creator\test-windows.txt"
  ```
- [ ] Trigger sync: `Start-ScheduledTask -TaskName "GitAutoSync-YokeAssets"`
- [ ] Check Windows log confirms push
- [ ] Wait 1-2 minutes
- [ ] On droplet, trigger sync: `/root/yoke-assets--github-/sync-repo.sh`
- [ ] Verify file exists: `cat "/root/yoke-assets--github-/claude code creator/test-windows.txt"`
- [ ] File should contain "test from windows"

#### 10. Test Droplet → Windows Sync
- [ ] On droplet, create test file:
  ```bash
  echo "test from droplet" > "/root/yoke-assets--github-/claude code creator/test-droplet.txt"
  ```
- [ ] Trigger sync: `/root/yoke-assets--github-/sync-repo.sh`
- [ ] Check droplet log confirms push: `tail -20 /root/yoke-assets-sync.log`
- [ ] Wait 1-2 minutes
- [ ] On Windows, trigger sync: `Start-ScheduledTask -TaskName "GitAutoSync-YokeAssets"`
- [ ] Verify file exists: `Get-Content "C:\Users\matth\Dropbox\Yoke Digital\yoke-assets--github-\claude code creator\test-droplet.txt"`
- [ ] File should contain "test from droplet"

#### 11. Verify Automatic Sync
- [ ] Wait 15 minutes without triggering manually
- [ ] Check Windows log shows automatic sync: `Get-Content sync-log.txt -Tail 5`
- [ ] Check droplet log shows automatic sync: `tail -5 /root/yoke-assets-sync.log`
- [ ] Both logs should have recent timestamps

---

## Setup Complete!

If all items are checked, your automated git sync system is fully operational.

### What Happens Now

- Every 15 minutes, both machines automatically:
  1. Pull latest changes from GitHub
  2. Commit changes in "claude code creator" folder
  3. Push commits to GitHub

- No manual intervention needed
- All activity logged
- Merge conflicts handled automatically

### Monitoring Commands

**Windows:**
```powershell
# View log
Get-Content "C:\Users\matth\Dropbox\Yoke Digital\yoke-assets--github-\sync-log.txt" -Tail 20

# Monitor in real-time
Get-Content "C:\Users\matth\Dropbox\Yoke Digital\yoke-assets--github-\sync-log.txt" -Tail 20 -Wait

# Check task status
Get-ScheduledTask -TaskName "GitAutoSync-YokeAssets"
```

**Droplet:**
```bash
# View log
tail -20 /root/yoke-assets-sync.log

# Monitor in real-time
tail -f /root/yoke-assets-sync.log

# Check cron
crontab -l
```

### Next Steps

- Monitor logs for a day or two
- Clean up test files once verified
- See `QUICK_REFERENCE.md` for common commands
- See `SYNC_SETUP_INSTRUCTIONS.md` for troubleshooting

---

## Notes

**Date Completed:** ________________

**Issues Encountered:**
-
-
-

**Resolution:**
-
-
-

**Additional Configuration:**
-
-
-
