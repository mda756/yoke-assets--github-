# Git Auto-Sync Setup Instructions

This guide will help you set up automated git syncing between your Windows PC and DigitalOcean droplet.

## Overview

The sync system will:
- Pull changes from GitHub every 15 minutes on both machines
- Automatically commit and push changes from the "claude code creator" folder
- Handle merge conflicts gracefully
- Log all activity for troubleshooting

---

## Part 1: GitHub SSH Setup

### Step 1: Add SSH Key to GitHub

Your new SSH public key has been generated:

```
ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIPJKr/cQAAeHS1FZLJPkM9GTWQv998dIurG1vFp5vVqR tech@yokedigital.com
```

**To add this to GitHub:**

1. Go to https://github.com/settings/keys
2. Click "New SSH key"
3. Title: `Windows PC - Yoke Digital`
4. Key type: `Authentication Key`
5. Paste the public key above
6. Click "Add SSH key"

### Step 2: Update Git Remote to Use SSH

Run this in PowerShell:

```powershell
cd "C:\Users\matth\Dropbox\Yoke Digital\yoke-assets--github-"
git remote set-url origin git@github.com:mda756/yoke-assets--github-.git
git remote -v
```

You should see:
```
origin  git@github.com:mda756/yoke-assets--github-.git (fetch)
origin  git@github.com:mda756/yoke-assets--github-.git (push)
```

### Step 3: Test SSH Connection

```powershell
ssh -T git@github.com
```

You should see: `Hi mda756! You've successfully authenticated...`

If you see a warning about the authenticity of the host, type `yes` to continue.

---

## Part 2: Handle Existing Changes

Before setting up automation, let's handle the existing untracked files.

### Option A: Keep All Untracked Files (Recommended)

This will commit everything:

```powershell
cd "C:\Users\matth\Dropbox\Yoke Digital\yoke-assets--github-"
git add .
git commit -m "Add all project files before setting up auto-sync"
git push origin main
```

### Option B: Ignore Some Files

Create or edit `.gitignore` to exclude files you don't want to sync:

```
# Add patterns for files to ignore
DEBUG/
temp_*.json
*.log
```

Then commit the rest:

```powershell
git add .
git commit -m "Add project files and update gitignore"
git push origin main
```

---

## Part 3: Windows Setup

### Step 1: Test the Sync Script

```powershell
cd "C:\Users\matth\Dropbox\Yoke Digital\yoke-assets--github-"
.\sync-repo.ps1
```

Check the log file:
```powershell
Get-Content "C:\Users\matth\Dropbox\Yoke Digital\yoke-assets--github-\sync-log.txt" -Tail 20
```

### Step 2: Set Up Task Scheduler

**Run PowerShell as Administrator**, then:

```powershell
cd "C:\Users\matth\Dropbox\Yoke Digital\yoke-assets--github-"
.\setup-windows-scheduler.ps1
```

This creates a scheduled task that runs every 15 minutes.

### Step 3: Test the Scheduled Task

```powershell
Start-ScheduledTask -TaskName "GitAutoSync-YokeAssets"
```

Then check the log again to verify it worked.

---

## Part 4: Droplet Setup

### Step 1: Connect to Droplet

```bash
ssh root@134.209.186.176
# Password: Digitalocan 2025Rootpassword75X
```

### Step 2: Set Up SSH Key for GitHub on Droplet

Generate SSH key on droplet:

```bash
ssh-keygen -t ed25519 -C "tech@yokedigital.com" -f ~/.ssh/id_ed25519 -N ""
cat ~/.ssh/id_ed25519.pub
```

**Add this new key to GitHub** (same process as Step 1):
1. Go to https://github.com/settings/keys
2. Click "New SSH key"
3. Title: `DigitalOcean Droplet - Yoke Digital`
4. Paste the public key
5. Click "Add SSH key"

### Step 3: Test SSH Connection on Droplet

```bash
ssh -T git@github.com
# Type 'yes' if prompted
```

### Step 4: Clone Repository (if not already present)

```bash
cd /root
git clone git@github.com:mda756/yoke-assets--github-.git
cd yoke-assets--github-
git config user.name "techyokedigital"
git config user.email "tech@yokedigital.com"
```

### Step 5: Copy Setup Scripts to Droplet

From your Windows PC, run:

```powershell
scp "C:\Users\matth\Dropbox\Yoke Digital\yoke-assets--github-\sync-repo.sh" root@134.209.186.176:/root/yoke-assets--github-/
scp "C:\Users\matth\Dropbox\Yoke Digital\yoke-assets--github-\setup-droplet-cron.sh" root@134.209.186.176:/root/yoke-assets--github-/
```

Password: `Digitalocan 2025Rootpassword75X`

### Step 6: Run Setup on Droplet

Back in your SSH session on the droplet:

```bash
cd /root/yoke-assets--github-
chmod +x setup-droplet-cron.sh
./setup-droplet-cron.sh
```

### Step 7: Test the Sync Script on Droplet

```bash
/root/yoke-assets--github-/sync-repo.sh
tail -20 /root/yoke-assets-sync.log
```

---

## Part 5: Verification

### On Windows:

```powershell
# View recent log entries
Get-Content "C:\Users\matth\Dropbox\Yoke Digital\yoke-assets--github-\sync-log.txt" -Tail 30

# Check scheduled task status
Get-ScheduledTask -TaskName "GitAutoSync-YokeAssets"

# View task history
Get-ScheduledTask -TaskName "GitAutoSync-YokeAssets" | Get-ScheduledTaskInfo
```

### On Droplet:

```bash
# View recent log entries
tail -30 /root/yoke-assets-sync.log

# Check cron job
crontab -l

# Monitor log in real-time
tail -f /root/yoke-assets-sync.log
```

---

## Troubleshooting

### SSH Connection Issues

If you get "Permission denied (publickey)":
1. Make sure you added the SSH key to GitHub
2. Test with: `ssh -T git@github.com`
3. Check that the key exists: `ls -la ~/.ssh/`

### Merge Conflicts

The scripts automatically handle conflicts by:
1. Stashing local changes
2. Pulling from origin
3. Re-applying stashed changes

If manual intervention is needed, check the log files.

### Script Not Running

**Windows:**
- Check Task Scheduler for error messages
- Verify the execution policy: `Get-ExecutionPolicy`
- Try running the script manually first

**Droplet:**
- Check cron is running: `systemctl status cron`
- Verify crontab: `crontab -l`
- Check system log: `grep CRON /var/log/syslog | tail -20`

### Permission Issues

**Windows:**
- Make sure you ran `setup-windows-scheduler.ps1` as Administrator

**Droplet:**
- Make sure scripts are executable: `chmod +x *.sh`
- Verify you're running as root

---

## Log Files

- **Windows:** `C:\Users\matth\Dropbox\Yoke Digital\yoke-assets--github-\sync-log.txt`
- **Droplet:** `/root/yoke-assets-sync.log`

These logs contain timestamps and detailed information about each sync operation.

---

## Testing the Full System

1. On Windows, create a test file in the "claude code creator" folder
2. Wait 15 minutes (or trigger the task manually)
3. Check the Windows log to confirm it was committed and pushed
4. Wait another 15 minutes for the droplet to pull
5. SSH into droplet and verify the file is there
6. Repeat in reverse (create file on droplet, wait, check Windows)

---

## Stopping or Disabling Sync

### Windows:

```powershell
# Disable the task
Disable-ScheduledTask -TaskName "GitAutoSync-YokeAssets"

# Re-enable it
Enable-ScheduledTask -TaskName "GitAutoSync-YokeAssets"

# Remove completely
Unregister-ScheduledTask -TaskName "GitAutoSync-YokeAssets" -Confirm:$false
```

### Droplet:

```bash
# Remove cron job
crontab -l | grep -v "sync-repo.sh" | crontab -

# Verify it's gone
crontab -l
```
