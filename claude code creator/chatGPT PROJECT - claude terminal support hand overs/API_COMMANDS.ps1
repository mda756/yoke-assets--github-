# PowerShell commands for Claude Code terminal
# Safe defaults: read/verify first; write only after you confirm.
# Requires WP Application Password auth.

# 0) Set credentials locally (DO NOT paste into chat)
# setx WP_USER "YokeAdmin"
# setx WP_APP_PASS "xxxx xxxx xxxx xxxx xxxx xxxx"
# Close + reopen terminal after setx OR use $env: for current session:
# $env:WP_USER="YokeAdmin"; $env:WP_APP_PASS="xxxx xxxx xxxx xxxx xxxx xxxx"

$Base = "https://yokehealth.com"
$Auth = "$env:WP_USER`:$env:WP_APP_PASS"

# 1) Verify auth
curl.exe -s -u $Auth "$Base/wp-json/wp/v2/users/me" | python -m json.tool

# 2) Verify page exists (ID 4148)
curl.exe -s -u $Auth "$Base/wp-json/wp/v2/pages/4148?context=edit" | python -m json.tool > page_4148.json

# 3) Confirm whether ACF fields are exposed in wp/v2 response
# Look for "acf" or "meta" keys in page_4148.json
python - <<'PY'
import json
d=json.load(open("page_4148.json","r",encoding="utf-8"))
print("keys:", sorted(d.keys()))
print("has_acf:", "acf" in d)
print("has_meta:", "meta" in d)
PY

# 4) Update TITLE only (safe)
# Title required by user: AI-powered publishing and learning proof 29-01-26 Draft
$NewTitle = "AI-powered publishing and learning proof 29-01-26 Draft"
$payload = @{ title = $NewTitle } | ConvertTo-Json
curl.exe -s -X POST -u $Auth "$Base/wp-json/wp/v2/pages/4148" -H "Content-Type: application/json" -d $payload | python -m json.tool

# 5) OPTIONAL: Read ACF field group exposure status (if your site supports ACF endpoints)
# If this returns rest_no_route, ignore and use wp/v2 with "acf" if present.
curl.exe -s -u $Auth "$Base/wp-json/acf/v3/pages/4148" | python -m json.tool

# 6) Bulk update ACF content (ONLY after field mapping is known)
# You must fill FIELD_MAPPING_TEMPLATE.md first.
# Then build a payload that updates only the editable layouts and leaves awards/testimonials untouched.
# Example shape (PLACEHOLDER - DO NOT RUN AS-IS):
# {
#   "acf": {
#     "panels": [
#       { "acf_fc_layout": "hero", "hero_heading": "...", "hero_subheading": "...", "hero_body": "..." },
#       { "acf_fc_layout": "content_panel", "title": "...", "body": "..." }
#     ]
#   }
# }
