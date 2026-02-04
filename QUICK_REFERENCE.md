# Git Auto-Sync Quick Reference

## Quick Setup (Fresh Start)

### Windows
```powershell
cd "C:\Users\matth\Dropbox\Yoke Digital\yoke-assets--github-"
.\SETUP-START-HERE.ps1
```

Follow the wizard prompts. It will guide you through everything.

---

## Manual Setup Steps

### 1. Add SSH Key to GitHub

**Key:** `ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIPJKr/cQAAeHS1FZLJPkM9GTWQv998dIurG1vFp5vVqR tech@yokedigital.com`

Add at: https://github.com/settings/keys

### 2. Commit Existing Changes
```powershell
cd "C:\Users\matth\Dropbox\Yoke Digital\yoke-assets--github-"
git add .
git commit -m "Initial commit before auto-sync"
git push origin main
```

### 3. Setup Windows Task Scheduler (As Admin)
```powershell
cd "C:\Users\matth\Dropbox\Yoke Digital\yoke-assets--github-"
.\setup-windows-scheduler.ps1
```

### 4. Setup Droplet
```bash
# Connect
ssh root@134.209.186.176
# Password: Digitalocan 2025Rootpassword75X

# Generate key
ssh-keygen -t ed25519 -C "tech@yokedigital.com" -f ~/.ssh/id_ed25519 -N ""
cat ~/.ssh/id_ed25519.pub
# Add this key to GitHub

# Test connection
ssh -T git@github.com

# Clone repo
cd /root
git clone git@github.com:mda756/yoke-assets--github-.git
cd yoke-assets--github-
git config user.name "techyokedigital"
git config user.email "tech@yokedigital.com"

# Setup cron
chmod +x setup-droplet-cron.sh
./setup-droplet-cron.sh
```

---

## Common Commands

### Windows

**View logs:**
```powershell
Get-Content "C:\Users\matth\Dropbox\Yoke Digital\yoke-assets--github-\sync-log.txt" -Tail 20
```

**Monitor logs in real-time:**
```powershell
Get-Content "C:\Users\matth\Dropbox\Yoke Digital\yoke-assets--github-\sync-log.txt" -Tail 20 -Wait
```

**Trigger sync manually:**
```powershell
Start-ScheduledTask -TaskName "GitAutoSync-YokeAssets"
```

**Check task status:**
```powershell
Get-ScheduledTask -TaskName "GitAutoSync-YokeAssets"
Get-ScheduledTask -TaskName "GitAutoSync-YokeAssets" | Get-ScheduledTaskInfo
```

**Disable auto-sync:**
```powershell
Disable-ScheduledTask -TaskName "GitAutoSync-YokeAssets"
```

**Enable auto-sync:**
```powershell
Enable-ScheduledTask -TaskName "GitAutoSync-YokeAssets"
```

**Remove auto-sync:**
```powershell
Unregister-ScheduledTask -TaskName "GitAutoSync-YokeAssets" -Confirm:$false
```

### Droplet

**View logs:**
```bash
tail -20 /root/yoke-assets-sync.log
```

**Monitor logs in real-time:**
```bash
tail -f /root/yoke-assets-sync.log
```

**Trigger sync manually:**
```bash
/root/yoke-assets--github-/sync-repo.sh
```

**Check cron job:**
```bash
crontab -l
```

**Disable auto-sync:**
```bash
crontab -l | grep -v "sync-repo.sh" | crontab -
```

**Re-enable auto-sync:**
```bash
cd /root/yoke-assets--github-
./setup-droplet-cron.sh
```

---

## File Locations

### Windows
- **Sync Script:** `C:\Users\matth\Dropbox\Yoke Digital\yoke-assets--github-\sync-repo.ps1`
- **Log File:** `C:\Users\matth\Dropbox\Yoke Digital\yoke-assets--github-\sync-log.txt`
- **SSH Key:** `C:\Users\matth\.ssh\id_ed25519`

### Droplet
- **Sync Script:** `/root/yoke-assets--github-/sync-repo.sh`
- **Log File:** `/root/yoke-assets-sync.log`
- **Repository:** `/root/yoke-assets--github-/`
- **SSH Key:** `/root/.ssh/id_ed25519`

---

## Troubleshooting

### "Permission denied (publickey)"
- SSH key not added to GitHub
- Go to https://github.com/settings/keys and add your key

### "merge conflict"
- Scripts handle this automatically
- Check logs if issues persist

### "Push rejected"
- Another machine pushed first
- Script will auto-retry after pulling

### Task not running (Windows)
- Check Task Scheduler for errors
- Verify execution policy: `Get-ExecutionPolicy`
- Run script manually to test

### Cron not running (Droplet)
- Check: `systemctl status cron`
- Verify: `crontab -l`
- Check logs: `grep CRON /var/log/syslog | tail -20`

---

## What Gets Synced

The scripts automatically commit and push changes from:
- **claude code creator/** folder (all files)

Everything else requires manual commits.

---

## Sync Schedule

Both machines sync every **15 minutes**:
- :00, :15, :30, :45 past each hour

---

## Testing the System

1. Create a test file:
   ```powershell
   # On Windows
   echo "test" > "C:\Users\matth\Dropbox\Yoke Digital\yoke-assets--github-\claude code creator\test.txt"
   ```

2. Wait 15 minutes or trigger manually:
   ```powershell
   Start-ScheduledTask -TaskName "GitAutoSync-YokeAssets"
   ```

3. Check Windows log:
   ```powershell
   Get-Content "C:\Users\matth\Dropbox\Yoke Digital\yoke-assets--github-\sync-log.txt" -Tail 20
   ```

4. Wait for droplet to pull (15 min or manual trigger)

5. Verify on droplet:
   ```bash
   ssh root@134.209.186.176
   cat /root/yoke-assets--github-/claude\ code\ creator/test.txt
   ```

---

## Getting Help

1. **Check logs first** (both Windows and Droplet)
2. **Test SSH connection:** `ssh -T git@github.com`
3. **Test sync script manually** before assuming automation is broken
4. **Check Task Scheduler / cron status**

Full documentation: `SYNC_SETUP_INSTRUCTIONS.md`
