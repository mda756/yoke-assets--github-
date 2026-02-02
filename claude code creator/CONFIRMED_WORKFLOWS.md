# Confirmed Workflows - Pre-Approved Actions

**Date Established:** 2026-01-29
**User:** Matt @ Yoke Digital
**Status:** ACTIVE - All workflows confirmed and approved

---

## Core Principle
**Work autonomously. Don't ask for sub-step confirmations.**
User wants fast, smooth, automated execution.

---

## 1. WORDPRESS PAGE EDITING - FULLY APPROVED

### What to do automatically:
✓ Read CREDENTIALS_STORE.json for WordPress credentials
✓ Access WordPress API without asking
✓ Edit pages when given page ID and instructions
✓ Update ACF fields directly
✓ Apply feedback files (CHANGELOG_FEEDBACK_vX.md) immediately
✓ Make content changes, styling updates, field modifications
✓ Stack/align buttons, adjust spacing, update text
✓ Create new pages when requested
✓ Clone/duplicate pages when requested

### Rules to follow:
- ALWAYS preserve Awards and Testimonials blocks (never touch them)
- After API updates, remind user to "Save Draft" in WP admin to regenerate cache
- Use ACF panels array structure for content updates
- Fix empty values (convert "" to null for validation)

### When to ask:
- Only if deleting entire pages
- Only if publishing to live (not draft)
- Only if user specifically asks for confirmation

---

## 2. APOLLO.IO - FULLY APPROVED

### What to do automatically:
✓ Read CREDENTIALS_STORE.json for Apollo API key
✓ Search for contacts/companies matching ICP criteria
✓ Create new contacts
✓ Update existing contacts
✓ Add/update ICP TYPE fields
✓ Create lists
✓ Add contacts to lists
✓ Create email sequences
✓ Add contacts to sequences
✓ Enrich contact data
✓ Export/analyze contact lists

### When to ask:
- Only if sending actual emails (review email content first)
- Only if deleting large batches of contacts (>50)
- Only if making changes to active/running sequences

---

## 3. FILE OPERATIONS - FULLY APPROVED

### What to do automatically:
✓ Create Python scripts for automation
✓ Create JSON files for API payloads
✓ Extract ZIP files in knowledge folders
✓ Read knowledge files and apply instructions
✓ Create/update credential files
✓ Create helper scripts and tools
✓ Save output files and logs

### When to ask:
- Only if deleting important files
- Only if overwriting files with "FINAL" or "MASTER" in name

---

## 4. PDF/DOCUMENT EDITING - FULLY APPROVED

### What to do automatically:
✓ Download and install PDF editing tools (e.g., PDFgear)
✓ Edit PDF content (dates, text, etc.)
✓ Extract images from SnagX files
✓ Read screenshots from "claude image drop folder"
✓ Overwrite original files when requested

---

## 5. CREDENTIALS MANAGEMENT - FULLY APPROVED

### What to do automatically:
✓ Store API keys and credentials in CREDENTIALS_STORE.json
✓ Add new services to credential store
✓ Read credentials automatically when needed
✓ Update credentials when provided

### Security rules:
- Never commit credentials to git
- Use application passwords (not main passwords)
- Keep credentials local only

---

## 6. KNOWLEDGE FILE PROCESSING - FULLY APPROVED

### What to do automatically:
✓ Extract and read ZIP files in "claude code creator" folder
✓ Apply PAGE_COPY.md content to WordPress pages
✓ Apply CHANGELOG_FEEDBACK files immediately
✓ Follow FIELD_MAPPING templates
✓ Execute instructions in knowledge files without asking

---

## 7. APOLLO ICP WORKFLOWS - FULLY APPROVED

### Available ICP Types (pre-confirmed):
- Medcoms agency
- Exec search - healthcare
- Exec search - General
- VC / PE target
- Partnership
- person of interest
- Publisher
- supplier

### What to do automatically:
✓ Tag contacts with ICP types
✓ Search for contacts by ICP
✓ Create ICP-specific lists
✓ Build sequences for ICP segments
✓ Filter and segment by ICP

---

## 8. WORDPRESS PAGE CREATION - FULLY APPROVED

### What to do automatically when user says "create new page":
1. Read any knowledge files provided (PAGE_COPY_vX.md, etc.)
2. Structure content into ACF panels (hero, two_col_panel, spacing, etc.)
3. Create page as draft
4. Apply all content from knowledge files
5. Set proper page title
6. Confirm completion with page ID and edit link

### Don't ask about:
- Panel structure
- Content formatting
- Draft vs publish (always draft unless specified)
- Spacing between sections
- Button styling/alignment

---

## 9. TODOIST - FULLY APPROVED

### What to do automatically:
✓ Read CREDENTIALS_STORE.json for Todoist API token
✓ Get tasks, projects, sections
✓ Create new tasks
✓ Update existing tasks
✓ Complete tasks
✓ Move tasks between projects
✓ Create subtasks (parent/child relationships)
✓ Add/update labels
✓ Set due dates and priorities
✓ Export task data

### When to ask:
- Only if deleting entire projects
- Only if completing large batches of tasks (>20)

---

## 10. TRELLO - FULLY APPROVED

### What to do automatically:
✓ Read CREDENTIALS_STORE.json for Trello API credentials
✓ Get boards, lists, cards
✓ Create new cards
✓ Update existing cards
✓ Move cards between lists
✓ Create checklists on cards
✓ Add checklist items
✓ Archive/delete cards when requested
✓ Add labels, due dates, descriptions
✓ Migrate content from other tools (Todoist, etc.)

### Rules to follow:
- When migrating tasks, confirm the target board and list
- For bulk operations, consolidate into checklists when appropriate
- Store frequently used board/list IDs in CREDENTIALS_STORE.json

### When to ask:
- Only if deleting entire boards
- Only if making changes to shared boards (unless explicitly instructed)

---

## 11. ALL TOOLS & CAPABILITIES - FULLY APPROVED

### Command Line / Bash - APPROVED
✓ Run any bash commands needed
✓ Install software/packages (npm, pip, curl, etc.)
✓ Execute Python scripts
✓ Run git commands
✓ File system operations (mkdir, cp, mv, rm)
✓ Download files with curl/wget
✓ Execute PowerShell commands on Windows

### Internet Access - APPROVED
✓ WebFetch - Access any URL to read content
✓ WebSearch - Search the web for information
✓ Look up documentation, APIs, examples
✓ Research companies, contacts, technologies
✓ Fetch data from public APIs
✓ Access GitHub, Stack Overflow, documentation sites

### File Operations - APPROVED
✓ Read any file in the workspace
✓ Write new files
✓ Edit existing files
✓ Delete files (except MASTER/FINAL files)
✓ Create folders/directories
✓ Move/rename files
✓ Extract ZIP/archives
✓ Read images, PDFs, documents

### API Access - APPROVED
✓ Call any API with provided credentials
✓ WordPress REST API
✓ Apollo.io API
✓ Any other API you provide credentials for
✓ Test API connections
✓ Debug API responses

### Automation Scripts - APPROVED
✓ Write Python automation scripts
✓ Create bash scripts
✓ Build tools and helpers
✓ Schedule tasks if needed
✓ Create workflows

### Research & Analysis - APPROVED
✓ Search the web for information
✓ Research ICP companies
✓ Look up contact information
✓ Find documentation
✓ Compare tools/services
✓ Analyze data and provide insights

**Bottom line:** Use any tool needed to complete the task. No permission required.

---

## 12. MULTI-STEP WORKFLOWS - FULLY APPROVED

### Example: "Create page from knowledge file"
✓ Extract ZIP → Read files → Parse content → Create page → Apply content → Confirm
**No sub-step confirmations needed**

### Example: "Apply feedback v2"
✓ Extract ZIP → Read changelog → Get page → Update fields → Apply changes → Verify
**No sub-step confirmations needed**

### Example: "Find medcoms agency contacts"
✓ Search Apollo → Filter by ICP → Create list → Add to sequence
**No sub-step confirmations needed**

---

## 13. ERROR HANDLING - APPROVED APPROACH

### What to do automatically:
✓ If API fails, try alternative approach
✓ If WordPress needs cache regeneration, remind user to save in admin
✓ If validation errors, fix data and retry
✓ If missing credentials, read from CREDENTIALS_STORE.json

### When to ask:
- If error is unclear and multiple solutions possible
- If data loss might occur

---

## QUICK REFERENCE

**User says → You do:**
- "Create page" → Create it (draft)
- "Apply feedback" → Apply it immediately
- "Find ICPs" → Search and return results
- "Update contact" → Update it
- "Create list" → Create it
- "Edit page 4148" → Read page, wait for instructions
- "Make these changes [knowledge file]" → Read file, apply all changes

**Never ask:**
- "Should I proceed?"
- "Is this correct?"
- "Do you want me to...?"

**Always do:**
- Execute immediately
- Confirm what was done
- Provide links/IDs for verification
- Note any manual steps needed (e.g., "Save in WP admin")

---

## 14. WEBSITE SCREENSHOT CAPTURE - FULLY APPROVED

### What to do automatically:
✓ Capture full-page screenshots of any website URL provided
✓ Use lazy-loading scroll technique to load all content
✓ Save screenshots to the working directory
✓ Name files based on domain name (e.g., nexgenhc_com_homepage.png)
✓ Use headless browser for faster capture

### Script to use:
`capture_website_screenshot.py <URL> [optional_filename]`

### Workflow:
1. User provides URL (e.g., "capture nexgenhc.com")
2. Run script to capture full-page screenshot with lazy loading
3. Save to working directory
4. Confirm filename and location
5. **User will manually upload to Miro themselves**

### Rules:
- ALWAYS use full-page screenshot (full_page=True)
- ALWAYS scroll to bottom first to trigger lazy loading
- Save in PNG format
- Keep files in working directory for user to upload manually

### When to ask:
- NEVER - just capture and save

### Example commands:
```bash
python capture_website_screenshot.py https://nexgenhc.com
python capture_website_screenshot.py https://example.com example_screenshot.png
```

---

## SESSION STARTUP

**At start of each new terminal session:**
1. Read CREDENTIALS_STORE.json automatically
2. Read this CONFIRMED_WORKFLOWS.md
3. Wait for user instruction
4. Execute without asking sub-steps

**User approval statement:**
"I have confirmed all these workflows. Execute autonomously without sub-step confirmations. Work fast and smooth."

---

**Last Updated:** 2026-01-29
**Status:** ACTIVE - No expiration
**Review:** Update this file if user adds new confirmed workflows
