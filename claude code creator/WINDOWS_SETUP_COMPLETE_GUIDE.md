# Complete Windows Setup Guide for Claude Code
## From Zero to Fully Operational

**Purpose:** Set up Claude Code CLI on a fresh Windows laptop with all credentials, knowledge store, and authorizations working.

**Starting Point:** PowerShell only, nothing else installed
**End Result:** Full Claude Code system identical to your main desktop

---

## Prerequisites Check

Open PowerShell as Administrator:
- Right-click Start menu → "Windows Terminal (Admin)" or "PowerShell (Admin)"

Check what you have:
```powershell
node --version   # Check if Node.js installed
git --version    # Check if Git installed
```

If you get "command not found" - that's fine, we'll install everything.

---

## Part 1: Install Required Software

### Step 1: Install Chocolatey (Package Manager for Windows)

In **PowerShell (Admin)**:

```powershell
Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
```

Close and reopen PowerShell as Admin after installation.

### Step 2: Install Git

```powershell
choco install git -y
```

Close and reopen PowerShell after installation.

Verify:
```powershell
git --version
```

### Step 3: Install Node.js (Required for Claude Code)

```powershell
choco install nodejs-lts -y
```

Close and reopen PowerShell after installation.

Verify:
```powershell
node --version
npm --version
```

Should show Node.js v20.x or higher.

### Step 4: Install Claude Code CLI

```powershell
npm install -g @anthropic-ai/claude-code
```

Verify:
```powershell
claude --version
```

---

## Part 2: Authenticate Claude Code

### Authenticate with Anthropic Account

```powershell
claude auth login
```

This will:
1. Open your browser
2. Ask you to log in to your Anthropic account
3. Authorize Claude Code CLI
4. Save authentication locally

**IMPORTANT:** Use the same Anthropic account you use on your main desktop.

---

## Part 3: Set Up Your Workspace

### Option A: Using Dropbox (Recommended - Auto-Sync)

**If Dropbox is already installed and syncing:**

1. Open PowerShell (regular, not admin):

```powershell
# Navigate to your Dropbox folder
cd "$env:USERPROFILE\Dropbox\Yoke Digital\yoke-assets--github-"

# Verify the structure exists
ls "claude code creator"
```

You should see:
- CREDENTIALS_STORE.json
- CONFIRMED_WORKFLOWS.md
- knowledge/ folder
- etc.

2. **You're done!** Everything is already synced via Dropbox.

3. Skip to Part 4.

---

### Option B: Using Git (If No Dropbox or Want Git Version Control)

**If you want to use Git instead:**

1. Set up Git repository on your main desktop first:

```powershell
# On your MAIN desktop
cd "C:\Users\matth\Dropbox\Yoke Digital\yoke-assets--github-"

# Initialize git (if not already)
git init

# Add everything
git add .

# Commit
git commit -m "Initial setup with credentials and knowledge store"

# Create a private GitHub repo and push
# (Or use GitLab, Bitbucket, etc.)
git remote add origin YOUR_PRIVATE_REPO_URL
git push -u origin main
```

2. Then on your HOME laptop:

```powershell
# Navigate to where you want the workspace
cd $env:USERPROFILE\Documents

# Clone the repository
git clone YOUR_PRIVATE_REPO_URL
cd yoke-assets--github-

# Verify structure
ls "claude code creator"
```

---

### Option C: Manual Copy (Not Recommended)

1. Copy the entire folder structure from your main desktop to a USB drive
2. Copy to your home laptop at: `C:\Users\YOUR_USERNAME\Documents\yoke-workspace`

---

## Part 4: Configure the Workspace

### Step 1: Update Session Hook Paths (If Needed)

The session-start hook has hardcoded paths. Update them for your laptop:

```powershell
# Open the hook file
notepad ".claude\hooks\session-start.sh"
```

**Update these lines** to match your laptop's username:

```bash
# Change from:
CREDENTIALS_FILE="C:/Users/matth/Dropbox/Yoke Digital/yoke-assets--github-/claude code creator/CREDENTIALS_STORE.json"

# To (replace YOUR_USERNAME):
CREDENTIALS_FILE="C:/Users/YOUR_USERNAME/Dropbox/Yoke Digital/yoke-assets--github-/claude code creator/CREDENTIALS_STORE.json"
```

Do the same for:
- `WORKFLOWS_FILE`
- `KNOWLEDGE_BASE`

**OR** use relative paths (better for portability):

```bash
# Get the script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
BASE_DIR="$( cd "$SCRIPT_DIR/../.." && pwd )"

CREDENTIALS_FILE="$BASE_DIR/claude code creator/CREDENTIALS_STORE.json"
WORKFLOWS_FILE="$BASE_DIR/claude code creator/CONFIRMED_WORKFLOWS.md"
KNOWLEDGE_BASE="$BASE_DIR/claude code creator/knowledge"
```

Save and close.

### Step 2: Make Hook Executable (If Using Git Bash)

If you have Git Bash:

```bash
chmod +x .claude/hooks/session-start.sh
```

In PowerShell, hooks should work automatically on Windows.

---

## Part 5: Test Everything

### Test 1: Navigate to Workspace

```powershell
# Using Dropbox path
cd "$env:USERPROFILE\Dropbox\Yoke Digital\yoke-assets--github-"

# OR if you cloned via Git
cd "$env:USERPROFILE\Documents\yoke-assets--github-"
```

### Test 2: Start Claude Code

```powershell
claude
```

**You should see:**
```
================================================
🚀 SESSION INITIALIZED - Credentials Loaded
================================================

📋 Available Services:
✓ Apollo.io API
✓ WordPress (yokehealth.com)
✓ Miro
✓ Todoist API
✓ Trello API (Yoke Master board)

📁 Credentials loaded from: CREDENTIALS_STORE.json

⚡ Workflow Mode: AUTONOMOUS
✓ CONFIRMED_WORKFLOWS.md loaded
✓ Pre-approved: WordPress, Apollo, Todoist, Trello, File Ops, PDFs
✓ No sub-step confirmations needed

================================================
💡 Ready to work. All credentials available.
================================================

<credentials>
{... credential data ...}
</credentials>

<knowledge_store>
{... knowledge data ...}
</knowledge_store>
```

### Test 3: Verify Credentials Loaded

In Claude Code, ask:
```
Can you confirm you have access to my Trello credentials?
```

Should respond with confirmation and show it has the API key/token.

### Test 4: Test a Simple Task

Ask Claude Code:
```
Add a test card to Show Girls in Trello called "Laptop Setup Test"
```

Should work immediately without asking for credentials.

---

## Part 6: Daily Usage on Home Laptop

### Starting a Session

1. Open PowerShell or Windows Terminal
2. Navigate to workspace:
   ```powershell
   cd "$env:USERPROFILE\Dropbox\Yoke Digital\yoke-assets--github-"
   ```
3. Start Claude Code:
   ```powershell
   claude
   ```
4. Everything loads automatically - credentials, knowledge, workflows

### Keeping in Sync

**If using Dropbox:**
- Automatic sync across all devices
- No manual steps needed

**If using Git:**
```powershell
# Before starting work - pull latest
git pull

# After making changes - commit and push
git add .
git commit -m "Updated ICP data"
git push
```

---

## Part 7: Troubleshooting

### Issue: "claude: command not found"

**Fix:**
```powershell
npm install -g @anthropic-ai/claude-code
```

Then close and reopen PowerShell.

### Issue: Session hook not running

**Check:**
```powershell
# Verify hook file exists
ls .claude\hooks\session-start.sh

# Verify permissions (in Git Bash)
chmod +x .claude/hooks/session-start.sh
```

### Issue: Credentials not loading

**Check paths in hook file:**
```powershell
notepad .claude\hooks\session-start.sh
```

Verify the paths match your laptop's folder structure.

**Or use relative paths** as shown in Part 4, Step 1.

### Issue: "Permission denied" on hooks

**In PowerShell Admin:**
```powershell
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Issue: Git not syncing

**Pull latest changes:**
```powershell
git pull origin main
```

**If conflicts:**
```powershell
git stash
git pull
git stash pop
```

---

## Part 8: Optional Enhancements

### Create PowerShell Alias for Quick Start

1. Open PowerShell profile:
```powershell
notepad $PROFILE
```

2. Add this:
```powershell
function Start-Claude {
    Set-Location "$env:USERPROFILE\Dropbox\Yoke Digital\yoke-assets--github-"
    claude
}

Set-Alias cc Start-Claude
```

3. Save and reload:
```powershell
. $PROFILE
```

4. Now you can just type:
```powershell
cc
```

From anywhere, and it will navigate to your workspace and start Claude Code.

### Install Windows Terminal (Better Than PowerShell)

```powershell
choco install microsoft-windows-terminal -y
```

Benefits:
- Multiple tabs
- Better UI
- Easier copy/paste
- Color themes

---

## Part 9: Verification Checklist

After setup, verify everything works:

- [ ] `node --version` shows v20.x or higher
- [ ] `git --version` shows Git is installed
- [ ] `claude --version` shows Claude Code is installed
- [ ] Claude Code authenticated (can start sessions)
- [ ] Workspace folder accessible (Dropbox or Git clone)
- [ ] Session hook runs on startup
- [ ] Credentials display in session start
- [ ] Knowledge store loads
- [ ] Can execute tasks (e.g., add Trello card) without providing credentials
- [ ] All workflows show as pre-approved

---

## Complete Setup Command Sequence

**Copy-paste this entire block into PowerShell Admin for automated setup:**

```powershell
# Install Chocolatey
Set-ExecutionPolicy Bypass -Scope Process -Force
[System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072
iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))

# Refresh environment
refreshenv

# Install Git and Node.js
choco install git nodejs-lts -y

# Refresh environment again
refreshenv

# Install Claude Code CLI
npm install -g @anthropic-ai/claude-code

Write-Host "Setup complete! Close and reopen PowerShell, then run: claude auth login"
```

---

## Quick Reference

### Essential Commands

```powershell
# Navigate to workspace
cd "$env:USERPROFILE\Dropbox\Yoke Digital\yoke-assets--github-"

# Start Claude Code
claude

# Verify installations
node --version
git --version
claude --version

# Update Claude Code
npm update -g @anthropic-ai/claude-code

# Pull latest changes (if using Git)
git pull

# Check Dropbox sync status
# (Open Dropbox app, check sync icon)
```

---

## File Structure After Setup

```
C:\Users\YOUR_USERNAME\
├── Dropbox\
│   └── Yoke Digital\
│       └── yoke-assets--github-\
│           ├── .claude\
│           │   ├── hooks\
│           │   │   └── session-start.sh
│           │   └── settings.local.json
│           ├── claude code creator\
│           │   ├── CREDENTIALS_STORE.json ← Your API keys
│           │   ├── CONFIRMED_WORKFLOWS.md ← Approved workflows
│           │   ├── LINUX_SERVER_SETUP_GUIDE.md
│           │   ├── WINDOWS_SETUP_COMPLETE_GUIDE.md ← This file
│           │   ├── add_knowledge.py
│           │   └── knowledge\
│           │       └── client_acquisition\
│           │           ├── icps/
│           │           ├── clients/
│           │           ├── landing_pages/
│           │           └── apollo/
│           └── [your project files]
```

---

## Summary

**What you installed:**
1. Chocolatey (package manager)
2. Git (version control)
3. Node.js (runtime for Claude Code)
4. Claude Code CLI

**What you configured:**
1. Authenticated Claude Code with your Anthropic account
2. Set up workspace with credentials and knowledge store
3. Configured session hooks for automatic loading

**What you can do now:**
- Start Claude Code from any home laptop
- All credentials load automatically
- All knowledge available (ICPs, clients, etc.)
- All workflows pre-approved (autonomous mode)
- Work seamlessly across main desktop and home laptops

---

**Document Location:** `claude code creator/WINDOWS_SETUP_COMPLETE_GUIDE.md`
**Created:** 2026-01-29
**Purpose:** Set up Claude Code on fresh Windows laptops with full system
