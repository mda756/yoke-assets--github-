# SSH Keys Reference Guide

**Created:** 2026-01-29
**Purpose:** Complete documentation of all SSH keys for Windows PC and Droplet

---

## Overview

SSH keys provide secure, password-free authentication for:
- GitHub repository access (push/pull without passwords)
- Droplet SSH access (more secure than passwords)
- Automated scripts and deployments

---

## Windows PC SSH Keys

### Location
**Public Key:** `C:\Users\matth\.ssh\id_ed25519.pub`
**Private Key:** `C:\Users\matth\.ssh\id_ed25519`

### Public Key Content
```
ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIMb4Vd433+RIZj8ZJjPS1i3IMBF8YatH4HT3UwPQcxrc tech@yokehealth.com
```

### Uses
- Git operations from Windows PC
- SSH to servers from Windows
- GitHub authentication

### Testing Key
```bash
# Test GitHub connection
ssh -T git@github.com

# Expected output:
# Hi [username]! You've successfully authenticated, but GitHub does not provide shell access.
```

### Viewing Keys on Windows
```bash
# View public key
cat C:\Users\matth\.ssh\id_ed25519.pub

# View private key (keep secure!)
cat C:\Users\matth\.ssh\id_ed25519
```

---

## Droplet SSH Keys

### Location
**Public Key:** `/root/.ssh/id_ed25519.pub`
**Private Key:** `/root/.ssh/id_ed25519`

### Current Status
**Status:** Needs to be generated

### Generating Droplet SSH Key

**Step 1: Connect to Droplet**
```bash
ssh root@134.209.186.176
# Password: Digitalocan 2025Rootpassword75X
```

**Step 2: Generate Key**
```bash
ssh-keygen -t ed25519 -C "tech@yokehealth.com"
```

**Prompts:**
```
Enter file in which to save the key (/root/.ssh/id_ed25519): [Press Enter]
Enter passphrase (empty for no passphrase): [Press Enter]
Enter same passphrase again: [Press Enter]
```

**Step 3: Display Public Key**
```bash
cat ~/.ssh/id_ed25519.pub
```

**Step 4: Copy the Output**
The key will look like:
```
ssh-ed25519 AAAA...long string...XYZ tech@yokehealth.com
```

---

## Adding SSH Keys to GitHub

### Why Add Keys to GitHub?
- Push/pull repositories without entering passwords
- More secure than HTTPS with passwords
- Required for automated scripts

### Adding Windows PC Key to GitHub

**1. Copy Public Key**
```bash
cat C:\Users\matth\.ssh\id_ed25519.pub
```

**2. Add to GitHub**
- Go to https://github.com/settings/keys
- Click "New SSH key"
- Title: "Windows PC - Matt"
- Key type: Authentication Key
- Paste the public key content
- Click "Add SSH key"

**3. Test Connection**
```bash
ssh -T git@github.com
```

### Adding Droplet Key to GitHub

**1. SSH to Droplet and Copy Key**
```bash
ssh root@134.209.186.176
cat ~/.ssh/id_ed25519.pub
```

**2. Add to GitHub**
- Go to https://github.com/settings/keys
- Click "New SSH key"
- Title: "DigitalOcean Droplet - Claude Code"
- Key type: Authentication Key
- Paste the public key content
- Click "Add SSH key"

**3. Test Connection (from Droplet)**
```bash
ssh -T git@github.com
```

---

## Using SSH Keys with Git

### On Windows PC

**Clone Repository (SSH)**
```bash
git clone git@github.com:username/repository.git
```

**Switch Existing Repo to SSH**
```bash
cd /path/to/repo
git remote set-url origin git@github.com:username/repository.git
```

**Verify Remote URL**
```bash
git remote -v
# Should show: git@github.com:username/repository.git
```

### On Droplet

**Same Commands Apply**
```bash
# Clone
git clone git@github.com:username/repository.git

# Configure Git (first time)
git config --global user.name "YokeHealth"
git config --global user.email "tech@yokehealth.com"

# Use normally
git add .
git commit -m "Update from droplet"
git push
# No password needed!
```

---

## SSH Key Types Comparison

### ED25519 (Recommended - Current)
- **Security:** Most secure modern algorithm
- **Speed:** Fastest
- **Size:** Smallest keys (public key ~68 characters)
- **Compatibility:** Supported by all modern systems
- **Command:** `ssh-keygen -t ed25519`

### RSA (Older Alternative)
- **Security:** Secure if 4096-bit
- **Speed:** Slower than ED25519
- **Size:** Larger keys
- **Compatibility:** Universal support (older systems)
- **Command:** `ssh-keygen -t rsa -b 4096`

**Recommendation:** Stick with ED25519 (already using)

---

## Testing SSH Keys

### Test GitHub Access

**From Windows:**
```bash
ssh -T git@github.com
```

**From Droplet:**
```bash
ssh root@134.209.186.176
ssh -T git@github.com
```

**Expected Output:**
```
Hi [username]! You've successfully authenticated, but GitHub does not provide shell access.
```

### Test Droplet Access with Key

**1. Copy Windows Key to Droplet (Optional)**
```bash
ssh-copy-id root@134.209.186.176
```

**2. Test Password-Free Login**
```bash
ssh root@134.209.186.176
# Should login without password prompt
```

---

## Security Best Practices

### Private Key Security
- **NEVER share private keys**
- **NEVER commit private keys to Git**
- **NEVER upload private keys to cloud storage**
- Private key file permissions should be 600 (read/write owner only)

### Public Keys
- **Safe to share** - it's called "public" for a reason
- Can be added to multiple services
- Can be regenerated if lost (with new private key)

### Key Passphrases
**Current Setup:** No passphrase (for convenience)

**Optional:** Add passphrase for extra security
- Requires password when using key
- More secure if key file is stolen
- Less convenient for automation

**To add passphrase to existing key:**
```bash
ssh-keygen -p -f ~/.ssh/id_ed25519
```

---

## Backup Important Keys

### What to Backup
- Windows private key: `C:\Users\matth\.ssh\id_ed25519`
- Windows public key: `C:\Users\matth\.ssh\id_ed25519.pub`
- Droplet private key: `/root/.ssh/id_ed25519` (once generated)

### Backup Command (Windows)
```bash
# Copy keys to secure backup location
cp C:\Users\matth\.ssh\id_ed25519* "C:\Users\matth\Dropbox\Yoke Digital\SECURE_BACKUPS\"
```

### Restore Keys
```bash
# Windows
cp "C:\Users\matth\Dropbox\Yoke Digital\SECURE_BACKUPS\id_ed25519*" C:\Users\matth\.ssh\

# Fix permissions
chmod 600 C:\Users\matth\.ssh\id_ed25519
chmod 644 C:\Users\matth\.ssh\id_ed25519.pub
```

---

## Troubleshooting

### "Permission denied (publickey)"

**Possible Causes:**
1. Key not added to GitHub
2. Using HTTPS URL instead of SSH
3. Wrong key permissions

**Solutions:**
```bash
# 1. Check GitHub keys: https://github.com/settings/keys

# 2. Check remote URL
git remote -v
# Should be: git@github.com:user/repo.git
# Not: https://github.com/user/repo.git

# 3. Fix permissions (Linux/Mac)
chmod 600 ~/.ssh/id_ed25519
chmod 644 ~/.ssh/id_ed25519.pub
```

### "Could not open a connection to your authentication agent"

**Solution (Windows):**
```bash
# Start SSH agent
eval $(ssh-agent)

# Add key
ssh-add C:\Users\matth\.ssh\id_ed25519
```

### Multiple SSH Keys

**If you have multiple keys for different services:**

Create `~/.ssh/config`:
```bash
# GitHub with specific key
Host github.com
  HostName github.com
  User git
  IdentityFile ~/.ssh/id_ed25519

# Droplet with specific key
Host droplet
  HostName 134.209.186.176
  User root
  IdentityFile ~/.ssh/droplet_key
```

---

## Quick Reference Commands

### Generate New Key
```bash
ssh-keygen -t ed25519 -C "tech@yokehealth.com"
```

### View Public Key
```bash
# Windows
cat C:\Users\matth\.ssh\id_ed25519.pub

# Droplet
cat ~/.ssh/id_ed25519.pub
```

### Test GitHub Connection
```bash
ssh -T git@github.com
```

### Copy Key to Server
```bash
ssh-copy-id root@134.209.186.176
```

### Add Key to SSH Agent
```bash
ssh-add ~/.ssh/id_ed25519
```

---

## Summary Checklist

### Windows PC
- [x] SSH key generated
- [x] Public key documented
- [x] Key added to GitHub (verify at https://github.com/settings/keys)
- [ ] Key backed up to secure location

### Droplet
- [ ] SSH key needs to be generated
- [ ] Public key needs to be added to GitHub
- [ ] Git configured with user info
- [ ] Test GitHub access successful

### GitHub
- [ ] Windows PC key added (title: "Windows PC - Matt")
- [ ] Droplet key added (title: "DigitalOcean Droplet - Claude Code")
- [ ] Both keys tested and working

---

**Document Version:** 1.0
**Last Updated:** 2026-01-29
**Next Review:** After generating droplet SSH key
