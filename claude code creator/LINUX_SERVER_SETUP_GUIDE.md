# Linux Cloud Server Setup Guide for Claude Code

**Purpose:** Run Claude Code CLI on a cloud server accessible from any device (Android, iOS, desktop, web).

---

## Why Use a Cloud Server?

✓ **Always on** - No need to keep home PC running
✓ **Access from anywhere** - Phone, tablet, any computer
✓ **Cost effective** - $5-10/month vs buying physical server
✓ **Professional infrastructure** - 99.9% uptime, fast connection
✓ **No maintenance** - No hardware to manage

---

## Cost Breakdown

**Recommended Specs:**
- 1-2 GB RAM
- 1 CPU core
- 25GB storage
- Ubuntu 22.04 LTS

**Providers:**
- DigitalOcean: $6/month (recommended - easiest)
- Linode: $5/month
- Vultr: $5/month
- Hetzner: $4/month (Europe-based)

---

## Part 1: Create the Server

### DigitalOcean Setup (Recommended)

1. **Sign up at digitalocean.com**
   - New users get $200 credit for 60 days

2. **Create a Droplet**
   - Click "Create" → "Droplets"
   - Choose: Ubuntu 22.04 LTS
   - Plan: Basic ($6/month - 1GB RAM)
   - Datacenter: Choose closest to you
   - Authentication: SSH Key (recommended) or Password
   - Hostname: `claude-code-server`

3. **Get your server IP**
   - After creation, note the IP address (e.g., 123.456.789.012)

---

## Part 2: Access Methods

### Option A: SSH Terminal Apps (Recommended for Mobile)

**Android:**
- **Termius** (best, free version works great)
  - Download from Play Store
  - Add new host
  - Enter IP, username (root), password/key
  - Save and connect

- **JuiceSSH** (alternative)
- **Termux** (full terminal emulator)

**iOS:**
- **Termius** (same app)
- **Blink Shell**
- **Prompt**

**Desktop:**
- Mac/Linux: Terminal app (built-in)
  ```bash
  ssh root@YOUR_SERVER_IP
  ```
- Windows: Windows Terminal or PuTTY

### Option B: Web Browser Access (No App Needed)

1. Log into DigitalOcean dashboard
2. Click on your Droplet
3. Click "Console" button
4. Terminal opens in browser
5. Works on ANY device

### Option C: VS Code Remote (Desktop Only - Most User-Friendly)

1. Install "Remote - SSH" extension in VS Code
2. Connect to server
3. Edit files with GUI, run commands in integrated terminal

---

## Part 3: Server Setup (One-Time)

### Step 1: Update System

```bash
apt update && apt upgrade -y
```

### Step 2: Install Node.js (Required for Claude Code)

```bash
curl -fsSL https://deb.nodesource.com/setup_20.x | bash -
apt install -y nodejs
node --version  # Should show v20.x
```

### Step 3: Install Claude Code CLI

```bash
npm install -g @anthropic-ai/claude-code
```

### Step 4: Authenticate Claude Code

```bash
claude auth login
```

Follow the prompts to authenticate with your Anthropic account.

### Step 5: Install Dropbox (For File Sync)

**Option A: Dropbox CLI (Headless)**

```bash
cd ~ && wget -O - "https://www.dropbox.com/download?plat=lnx.x86_64" | tar xzf -
~/.dropbox-dist/dropboxd &
```

Link your account:
```bash
# It will give you a URL to visit for authentication
```

**Option B: Rclone (Alternative)**

```bash
apt install rclone -y
rclone config  # Follow prompts to add Dropbox
rclone sync dropbox:"/Yoke Digital/yoke-assets--github-" ~/yoke-workspace
```

### Step 6: Set Up Your Workspace

```bash
# Create working directory
mkdir -p ~/yoke-workspace
cd ~/yoke-workspace

# If using Dropbox CLI, create symlink
ln -s ~/Dropbox/Yoke\ Digital/yoke-assets--github-/ ~/yoke-workspace

# Or if using rclone, sync manually
rclone sync dropbox:"/Yoke Digital/yoke-assets--github-" ~/yoke-workspace
```

### Step 7: Configure Claude Code Hooks

```bash
cd ~/yoke-workspace
chmod +x .claude/hooks/session-start.sh
```

### Step 8: Test Everything

```bash
cd ~/yoke-workspace
claude
```

You should see the session-start hook output with:
- Credentials loaded
- Knowledge store loaded
- All services available

---

## Part 4: Daily Usage

### From Phone (Android/iOS)

1. Open Termius (or your SSH app)
2. Tap your saved connection
3. Connect (auto-login with saved credentials)
4. Run:
   ```bash
   cd ~/yoke-workspace
   claude
   ```
5. Start working with Claude Code

### From Desktop

1. Open Terminal/SSH client
2. SSH into server:
   ```bash
   ssh root@YOUR_SERVER_IP
   ```
3. Navigate and run:
   ```bash
   cd ~/yoke-workspace
   claude
   ```

### From Web Browser

1. Log into DigitalOcean
2. Click "Console" on your Droplet
3. Terminal opens in browser
4. Run Claude Code as above

---

## Part 5: Keeping Files in Sync

### Option A: Auto-Sync with Dropbox

If you set up Dropbox CLI, it syncs automatically.

### Option B: Manual Sync with Rclone

Create a sync script:

```bash
nano ~/sync-dropbox.sh
```

Add:
```bash
#!/bin/bash
rclone sync dropbox:"/Yoke Digital/yoke-assets--github-" ~/yoke-workspace
rclone sync ~/yoke-workspace dropbox:"/Yoke Digital/yoke-assets--github-"
```

Make executable:
```bash
chmod +x ~/sync-dropbox.sh
```

Run before/after Claude Code sessions:
```bash
~/sync-dropbox.sh
```

### Option C: Cron Job (Automatic Every Hour)

```bash
crontab -e
```

Add:
```
0 * * * * ~/sync-dropbox.sh
```

---

## Part 6: Security Best Practices

### 1. Create Non-Root User (Recommended)

```bash
adduser yourusername
usermod -aG sudo yourusername
```

### 2. Set Up SSH Key Authentication (Disable Password)

```bash
# On your local machine, generate key if you don't have one
ssh-keygen -t ed25519

# Copy to server
ssh-copy-id root@YOUR_SERVER_IP

# On server, disable password auth
nano /etc/ssh/sshd_config
# Set: PasswordAuthentication no
systemctl restart sshd
```

### 3. Set Up Firewall

```bash
ufw allow 22/tcp  # SSH
ufw enable
```

---

## Part 7: Troubleshooting

### Can't Connect to Server
- Check server is running in DigitalOcean dashboard
- Verify IP address
- Check firewall allows port 22

### Claude Code Not Found
```bash
npm install -g @anthropic-ai/claude-code
```

### Dropbox Not Syncing
```bash
# Check Dropbox status
dropbox status

# Or re-run rclone sync
~/sync-dropbox.sh
```

### Session Hook Not Running
```bash
chmod +x .claude/hooks/session-start.sh
```

---

## Cost Summary

**Monthly Costs:**
- Server: $5-10/month
- Dropbox: (you already have this)
- **Total: $5-10/month**

**Benefits:**
- Access from any device
- Always available
- No home PC needed
- Professional infrastructure

---

## Quick Reference Commands

```bash
# Connect to server
ssh root@YOUR_SERVER_IP

# Navigate to workspace
cd ~/yoke-workspace

# Sync Dropbox (if using rclone)
~/sync-dropbox.sh

# Start Claude Code
claude

# Check server resources
htop  # (install: apt install htop)

# Check disk space
df -h
```

---

## Next Steps After Setup

1. ✓ Server created and accessible
2. ✓ Claude Code installed
3. ✓ Dropbox synced
4. ✓ Knowledge store loaded
5. → Start using Claude Code from any device
6. → Add ICPs, clients, and landing pages to knowledge store
7. → Work seamlessly across all devices

---

**Document Location:** `claude code creator/LINUX_SERVER_SETUP_GUIDE.md`
**Created:** 2026-01-29
**Status:** Ready to use when you want to set up cloud server
