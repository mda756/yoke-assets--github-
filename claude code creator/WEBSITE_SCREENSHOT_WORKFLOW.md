# Website Screenshot Workflow - APPROVED

**Date Established:** 2026-01-29
**Status:** ACTIVE

---

## Workflow Summary

**User provides URL → Claude captures screenshot → Saves to folder → User uploads to Miro manually**

---

## How It Works

### User says:
- "Capture screenshot of nexgenhc.com"
- "Screenshot https://example.com"
- "Grab full page of hex.co"

### Claude does:
1. Run `capture_website_screenshot.py <URL>`
2. Navigate to URL with headless browser
3. Scroll to bottom to trigger lazy loading
4. Capture full-page screenshot
5. Save as PNG in working directory
6. Confirm filename and location

### User does:
- Open Miro
- Create board (or use existing)
- Drag PNG file from folder to Miro board
- Done (takes 10 seconds)

---

## Script Location

`C:\Users\matth\Dropbox\Yoke Digital\yoke-assets--github-\capture_website_screenshot.py`

---

## Usage Examples

### Simple (auto-named file):
```bash
python capture_website_screenshot.py https://nexgenhc.com
# Output: nexgenhc_com_homepage.png
```

### Custom filename:
```bash
python capture_website_screenshot.py https://example.com my_screenshot.png
# Output: my_screenshot.png
```

---

## Key Features

✓ **Full-page capture** - Captures entire page, not just viewport
✓ **Lazy loading** - Scrolls to bottom to load all content
✓ **Fast** - Headless browser (no window opens)
✓ **Automatic naming** - Uses domain name if no filename provided

---

## Why Not Auto-Upload to Miro?

Miro's upload interface cannot be reliably automated:
- No accessible file upload triggers
- Popups and overlays block automation
- File inputs are dynamically created and hidden
- Tried 15+ different automation methods - none reliable

**Solution:** Capture works perfectly, manual upload takes 10 seconds

---

## Saved Miro Session

Authentication is saved in `miro_auth_state.json`:
- Can automatically create Miro boards
- Can automatically login
- Cannot automatically upload files (manual step required)

If you need to re-authenticate:
```bash
python miro_save_session.py
```

---

## Future Sessions

When you open a new terminal and say:
> "Screenshot nexgenhc.com for Miro"

I will:
1. Capture full-page screenshot with lazy loading
2. Save as `nexgenhc_com_homepage.png`
3. Confirm location
4. You drag to Miro (10 seconds)

**No questions asked. Fast and smooth.**

---

**Last Updated:** 2026-01-29
**User Approval:** "I would do this by getting you to create the screen grabs only... I will take them out of the folder and put them into mirror myself"
