# Complete Droplet Setup Guide

**Created:** 2026-01-29
**Purpose:** Full documentation for accessing and using the DigitalOcean droplet for Claude Code from any device

---

## Server Details

### Access Information
- **IP Address:** 134.209.186.176
- **Username:** root
- **Password:** Digitalocan 2025Rootpassword75X
- **Provider:** DigitalOcean
- **Datacenter:** London (lon1)
- **Plan:** Basic - 1 vCPU, 1GB RAM, 25GB SSD

### Operating System
- **OS:** Ubuntu 24.04.3 LTS (Noble Numbat)
- **Kernel:** Linux 6.8.0-71-generic
- **Architecture:** x86_64

---

## Installed Software Versions

### Core Software
- **Python:** Python 3.x (system default)
- **Node.js:** v20.x
- **NPM:** v10.x
- **Git:** Latest stable version
- **tmux:** Latest stable version

### Development Tools
- **Claude Code CLI:** @anthropic-ai/claude-code (installed globally)
- **Playwright:** For browser automation
- **Curl:** For API requests

---

## SSH Keys

### Windows PC SSH Key
**Location:** `C:\Users\matth\.ssh\id_ed25519.pub`

```
ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIMb4Vd433+RIZj8ZJjPS1i3IMBF8YatH4HT3UwPQcxrc tech@yokehealth.com
```

**Private Key:** `C:\Users\matth\.ssh\id_ed25519`

### Droplet SSH Key
**Status:** Key needs to be generated on droplet for GitHub access

**To generate on droplet:**
```bash
ssh-keygen -t ed25519 -C "tech@yokehealth.com"
cat ~/.ssh/id_ed25519.pub
```

Then add to GitHub: https://github.com/settings/keys

---

## Access Instructions

### From Windows PC

**Method 1: Direct SSH**
```bash
ssh root@134.209.186.176
# Enter password: Digitalocan 2025Rootpassword75X
```

**Method 2: Windows Terminal with SSH**
```bash
# Open Windows Terminal
ssh root@134.209.186.176
```

**Method 3: VS Code Remote SSH**
1. Install "Remote - SSH" extension
2. Press F1, type "Remote-SSH: Connect to Host"
3. Enter: `root@134.209.186.176`
4. Enter password when prompted

### From Android Phone

**Recommended: Termius App**
1. Download Termius from Play Store
2. Add new host:
   - Host: 134.209.186.176
   - Username: root
   - Password: Digitalocan 2025Rootpassword75X
3. Save and connect

**Alternative: JuiceSSH**
Similar setup process

### From iOS Devices

**Recommended: Termius App**
Same setup as Android version

**Alternative: Blink Shell**
Professional terminal emulator

### From Web Browser (Any Device)

1. Go to https://cloud.digitalocean.com
2. Log into your DigitalOcean account
3. Click on "Droplets" in left menu
4. Click on your droplet name
5. Click "Console" button (top right)
6. Terminal opens in browser - no app needed

---

## Workspace Setup

### Directory Structure
```
/root/
├── yoke-workspace/
│   └── claude-code-creator/
│       └── CREDENTIALS_STORE.json
└── .ssh/
    ├── id_ed25519 (to be created)
    └── id_ed25519.pub (to be created)
```

### Synced Files Location
**Windows:** `C:\Users\matth\Dropbox\Yoke Digital\yoke-assets--github-\claude code creator\`

**Droplet:** `~/yoke-workspace/claude-code-creator/`

---

## Git Setup (No Passwords Needed)

### On Droplet

**1. Generate SSH Key (if not already done)**
```bash
ssh-keygen -t ed25519 -C "tech@yokehealth.com"
# Press Enter for all prompts (no passphrase)
```

**2. Display Public Key**
```bash
cat ~/.ssh/id_ed25519.pub
```

**3. Add to GitHub**
- Go to https://github.com/settings/keys
- Click "New SSH key"
- Paste the public key
- Title: "Droplet - Claude Code"

**4. Test Connection**
```bash
ssh -T git@github.com
# Should see: Hi [username]! You've successfully authenticated
```

**5. Configure Git**
```bash
git config --global user.name "YokeHealth"
git config --global user.email "tech@yokehealth.com"
```

**6. Clone/Pull Repositories**
```bash
# Clone using SSH URL (not HTTPS)
git clone git@github.com:username/repo.git

# No password needed - uses SSH key
```

---

## Using tmux (Session Management)

### Why Use tmux?
- Keep Claude Code sessions running when you disconnect
- Resume exactly where you left off
- Multiple windows/panes in one terminal

### Basic tmux Commands

**Start New Session**
```bash
tmux new -s claude
```

**Detach from Session (keep it running)**
```
Press: Ctrl+b, then d
```

**List Sessions**
```bash
tmux ls
```

**Reattach to Session**
```bash
tmux attach -t claude
```

**Kill Session**
```bash
tmux kill-session -t claude
```

### Common Use Case
```bash
# SSH into droplet
ssh root@134.209.186.176

# Start tmux session
tmux new -s work

# Navigate to workspace
cd ~/yoke-workspace

# Start Claude Code
claude

# Work with Claude...

# Detach when done: Ctrl+b, then d
# Disconnect from SSH - session keeps running

# Later: SSH back in and reattach
tmux attach -t work
# Your Claude session is exactly as you left it
```

---

## Quick Start Commands

### Daily Workflow

**Connect and Start Working**
```bash
# 1. SSH to droplet
ssh root@134.209.186.176

# 2. Start or attach tmux session
tmux attach -t claude || tmux new -s claude

# 3. Navigate to workspace
cd ~/yoke-workspace/claude-code-creator

# 4. Start Claude Code
claude

# 5. Work normally...

# 6. When done - detach: Ctrl+b, then d
# 7. Exit SSH: exit
```

### File Management

**View Credentials**
```bash
cat ~/yoke-workspace/claude-code-creator/CREDENTIALS_STORE.json
```

**Edit Files**
```bash
nano ~/yoke-workspace/claude-code-creator/CREDENTIALS_STORE.json
```

**Sync Files (manual)**
```bash
# Copy from Windows to Droplet
scp "C:\Users\matth\Dropbox\Yoke Digital\yoke-assets--github-\claude code creator\CREDENTIALS_STORE.json" root@134.209.186.176:~/yoke-workspace/claude-code-creator/

# Copy from Droplet to Windows
scp root@134.209.186.176:~/yoke-workspace/claude-code-creator/CREDENTIALS_STORE.json "C:\Users\matth\Dropbox\Yoke Digital\yoke-assets--github-\claude code creator\"
```

### System Commands

**Check System Resources**
```bash
# CPU and Memory usage
htop

# Disk usage
df -h

# Check running processes
ps aux | grep claude
```

**Update System**
```bash
apt update && apt upgrade -y
```

**Restart Services**
```bash
# Restart SSH (if needed)
systemctl restart sshd
```

---

## Troubleshooting

### Can't Connect via SSH
1. Check internet connection
2. Verify IP: 134.209.186.176
3. Check DigitalOcean dashboard - droplet is running
4. Try web console as backup

### Claude Code Not Working
```bash
# Reinstall Claude Code
npm install -g @anthropic-ai/claude-code

# Check authentication
claude auth status
claude auth login
```

### Session Not Persisting
```bash
# Make sure you're using tmux
tmux new -s claude

# Always detach (don't exit)
# Press: Ctrl+b, then d
```

### Files Not Found
```bash
# Check workspace exists
ls -la ~/yoke-workspace/

# Recreate if needed
mkdir -p ~/yoke-workspace/claude-code-creator

# Copy credentials from Windows
scp "C:\Users\matth\Dropbox\Yoke Digital\yoke-assets--github-\claude code creator\CREDENTIALS_STORE.json" root@134.209.186.176:~/yoke-workspace/claude-code-creator/
```

### Git Push Denied
```bash
# Generate SSH key if not done
ssh-keygen -t ed25519 -C "tech@yokehealth.com"

# Show public key
cat ~/.ssh/id_ed25519.pub

# Add to GitHub: https://github.com/settings/keys

# Test connection
ssh -T git@github.com
```

---

## Security Notes

### Current Setup
- Password authentication enabled (for ease of access)
- Root user access (for full control)
- No firewall restrictions (SSH port 22 open)

### Optional Security Improvements

**1. Add SSH Key Authentication**
```bash
# On Windows, copy your public key to droplet
ssh-copy-id root@134.209.186.176

# Then disable password auth (optional)
nano /etc/ssh/sshd_config
# Set: PasswordAuthentication no
systemctl restart sshd
```

**2. Create Non-Root User**
```bash
adduser yoke
usermod -aG sudo yoke
# Then use this user instead of root
```

**3. Set Up Firewall**
```bash
ufw allow 22/tcp
ufw enable
```

---

## Backup Strategy

### Important Files to Backup
- `~/yoke-workspace/claude-code-creator/CREDENTIALS_STORE.json`
- `~/.ssh/id_ed25519` (private key)
- `~/.ssh/id_ed25519.pub` (public key)

### Backup Command
```bash
# Create backup archive
tar -czf ~/backup-$(date +%Y%m%d).tar.gz ~/yoke-workspace ~/.ssh

# Copy to Windows
scp root@134.209.186.176:~/backup-*.tar.gz "C:\Users\matth\Dropbox\Yoke Digital\"
```

---

## Cost Information

**Monthly Cost:** $6/month (DigitalOcean Basic Droplet)

**Included:**
- 1 vCPU
- 1GB RAM
- 25GB SSD storage
- 1TB transfer
- 99.99% uptime SLA

---

## Next Steps

1. Generate SSH key on droplet for GitHub access
2. Set up automated backup to Dropbox
3. Install additional tools as needed
4. Consider upgrading to 2GB RAM if needed ($12/month)

---

**Document Version:** 1.0
**Last Updated:** 2026-01-29
**Maintained By:** Matt @ Yoke Health
