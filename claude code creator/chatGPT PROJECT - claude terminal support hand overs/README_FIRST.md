PROJECT MODE (for Claude Code terminal)

Output format:
YES/NO
NEXT ACTION: <single best next step>

Permission gate:
No installs, no plugin changes, no publishing, no destructive writes without explicit user permission.

Credentials:
Never paste credentials into chat.
Use env vars locally (PowerShell) for WP_USER and WP_APP_PASS.

Editing approach:
- Prefer REST API updates of ACF fields once exposed.
- If ACF fields are not exposed, edit manually in wp-admin (ACF UI) using PAGE_COPY.md.
