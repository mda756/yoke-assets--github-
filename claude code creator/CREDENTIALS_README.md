# Credentials Store

This folder contains persistent credentials for Claude Code to access various services.

## Files:
- **CREDENTIALS_STORE.json** - Main credentials file (DO NOT COMMIT TO GIT)
- **CREDENTIALS_README.md** - This file

## Current Services:

### Apollo.io
- **Purpose:** Lead generation, contact search, email sequences
- **Access:** Full API access via API key
- **Capabilities:** Search people/companies, create lists, manage sequences

### WordPress (yokehealth.com)
- **Purpose:** Page editing, content management
- **Access:** REST API + ACF via application password
- **Capabilities:** Edit pages, update ACF fields, manage content

## Usage:
When Claude needs credentials, it will read from `CREDENTIALS_STORE.json` automatically.

## Adding New Services:
Add new service entries to the "services" object in CREDENTIALS_STORE.json following the same structure.

## Security:
- Keep this file local only
- Add to .gitignore if using version control
- Rotate credentials periodically
- Use application-specific passwords when possible (not main passwords)

## Last Updated:
2026-01-29
