# Droplet Sync Setup Guide

Your knowledge base is now synced to GitHub at: `https://github.com/mda756/yoke-assets--github-`

## What's Done ✓

1. **GitHub Desktop Auto-Start** - Launches automatically when Windows starts
2. **Local Git Repository** - Your folder is tracked and synced with GitHub
3. **GitHub Repository** - Connected to `mda756/yoke-assets--github-`
4. **Sensitive Files Protected** - Added .gitignore to exclude credentials

## Setting Up Your Droplet

### 1. SSH into Your Droplet

```bash
ssh root@YOUR_DROPLET_IP
```

### 2. Clone the Repository

```bash
cd ~
git clone https://github.com/mda756/yoke-assets--github-.git
cd yoke-assets--github-
```

### 3. Navigate to Your Knowledge Base

```bash
cd "claude code creator"
```

## Daily Workflow

### On Your PC (Making Changes)

1. Edit files in: `C:\Users\matth\Dropbox\Yoke Digital\yoke-assets--github-\claude code creator`
2. Stage and commit changes:
   ```bash
   git add .
   git commit -m "Update knowledge base"
   git push origin main
   ```

   OR use GitHub Desktop (easier):
   - Open GitHub Desktop
   - Review changes
   - Write commit message
   - Click "Commit to main"
   - Click "Push origin"

### On Your Droplet (Getting Updates)

```bash
cd ~/yoke-assets--github-
git pull origin main
```

### From Droplet to PC

If you make changes on the droplet:

```bash
cd ~/yoke-assets--github-
git add .
git commit -m "Update from droplet"
git push origin main
```

Then on your PC:
```bash
cd "C:\Users\matth\Dropbox\Yoke Digital\yoke-assets--github-"
git pull origin main
```

## Quick Reference

- **Your Local Folder**: `C:\Users\matth\Dropbox\Yoke Digital\yoke-assets--github-\claude code creator`
- **GitHub Repo**: `https://github.com/mda756/yoke-assets--github-`
- **Knowledge Files**: `claude code creator/knowledge/`

## Important Notes

- **Credentials are protected** - Files with secrets won't be pushed to GitHub
- **Dropbox + Git** - This folder is in Dropbox, so you have double backup
- **Auto-sync** - GitHub Desktop starts automatically with Windows
- **Access anywhere** - Clone the repo on any machine to access your knowledge base

## Troubleshooting

### Can't push from PC?
```bash
cd "C:\Users\matth\Dropbox\Yoke Digital\yoke-assets--github-"
git status
git pull origin main
# Fix any conflicts, then:
git push origin main
```

### Can't pull on droplet?
```bash
cd ~/yoke-assets--github-
git status
# If you have local changes:
git stash
git pull origin main
git stash pop
```

### Need to check what's different?
```bash
git diff
git status
```
