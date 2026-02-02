# Claude Code Knowledge Base Setup

## Purpose
This repository contains your business knowledge base for Claude Code, including:
- ICP definitions and client acquisition framework
- WordPress workflow documentation
- Miro integration guides
- Apollo.io integration and connectors
- Client management schemas and processes

## Setup on Any Device

### 1. Clone the Repository
```bash
git clone https://github.com/mda756/yoke-assets--github-.git
cd yoke-assets--github-
```

### 2. For Claude Code Access

When starting a new Claude Code session, provide context by saying:
```
Load my knowledge base from ./knowledge and read the following key files:
- QUICK_START_GUIDE.md
- CONFIRMED_WORKFLOWS.md
- knowledge/client_acquisition/_OVERVIEW.md
- knowledge/client_acquisition/_SCHEMAS.json
```

Or simply say:
```
I have a knowledge base in this directory. Read the setup guides and knowledge folder to understand my business context.
```

### 3. Keep It Synced

Before starting work:
```bash
git pull
```

After making changes:
```bash
git add .
git commit -m "Update knowledge base"
git push
```

## Key Files to Reference

### Business Context
- `knowledge/client_acquisition/_OVERVIEW.md` - Client acquisition flow
- `knowledge/client_acquisition/_SCHEMAS.json` - Data structures
- `CONFIRMED_WORKFLOWS.md` - Approved processes

### WordPress
- `WEBSITE_SCREENSHOT_WORKFLOW.md` - WordPress workflows
- `chatGPT PROJECT - claude terminal support hand overs/WP_TERMS_GLOSSARY.md` - WordPress terminology

### Apollo
- `APOLLO_M3_CONTACTS.md` - Apollo contacts and usage
- `chatGPT PROJECT - claude terminal support hand overs/API_COMMANDS.ps1` - API commands

### Server Setup
- `LINUX_SERVER_SETUP_GUIDE.md` - Linux server configuration
- `WINDOWS_SETUP_COMPLETE_GUIDE.md` - Windows setup
- `DROPLET_COMPLETE_SETUP.md` - DigitalOcean droplet setup

## Security Note
Sensitive files (credentials, keys) are excluded via `.gitignore` and must be managed separately.
