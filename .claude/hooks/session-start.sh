#!/bin/bash

# Claude Code Session Startup Hook
# Auto-loads credentials and workflows at session start

CREDENTIALS_FILE="C:/Users/matth/Dropbox/Yoke Digital/yoke-assets--github-/claude code creator/CREDENTIALS_STORE.json"
WORKFLOWS_FILE="C:/Users/matth/Dropbox/Yoke Digital/yoke-assets--github-/claude code creator/CONFIRMED_WORKFLOWS.md"

echo "================================================"
echo "🚀 SESSION INITIALIZED - Credentials Loaded"
echo "================================================"
echo ""
echo "📋 Available Services:"

if [ -f "$CREDENTIALS_FILE" ]; then
    echo "✓ Apollo.io API"
    echo "✓ WordPress (yokehealth.com)"
    echo "✓ Miro"
    echo "✓ Todoist API"
    echo "✓ Trello API (Yoke Master board)"
    echo ""
    echo "📁 Credentials loaded from: CREDENTIALS_STORE.json"
else
    echo "⚠️  CREDENTIALS_STORE.json not found"
fi

echo ""
echo "⚡ Workflow Mode: AUTONOMOUS"

if [ -f "$WORKFLOWS_FILE" ]; then
    echo "✓ CONFIRMED_WORKFLOWS.md loaded"
    echo "✓ Pre-approved: WordPress, Apollo, Todoist, Trello, File Ops, PDFs"
    echo "✓ No sub-step confirmations needed"
else
    echo "⚠️  CONFIRMED_WORKFLOWS.md not found"
fi

echo ""
echo "================================================"
echo "💡 Ready to work. All credentials available."
echo "================================================"
echo ""

# Output the actual credential content for Claude to read
if [ -f "$CREDENTIALS_FILE" ]; then
    echo "<credentials>"
    cat "$CREDENTIALS_FILE"
    echo "</credentials>"
fi

# Output key workflow info for Claude to read
if [ -f "$WORKFLOWS_FILE" ]; then
    echo "<workflows>"
    echo "AUTONOMOUS MODE ACTIVE - Execute without asking sub-steps"
    echo "Approved services: WordPress, Apollo.io, Todoist, Trello, Miro"
    echo "See full workflows in CONFIRMED_WORKFLOWS.md"
    echo "</workflows>"
fi

# Load Knowledge Store
KNOWLEDGE_BASE="C:/Users/matth/Dropbox/Yoke Digital/yoke-assets--github-/claude code creator/knowledge"
if [ -d "$KNOWLEDGE_BASE" ]; then
    echo "<knowledge_store>"
    echo "Knowledge store location: $KNOWLEDGE_BASE"
    echo ""

    # Load all JSON files from client_acquisition
    echo "=== CLIENT ACQUISITION KNOWLEDGE ==="

    # ICPs
    if [ -d "$KNOWLEDGE_BASE/client_acquisition/icps" ]; then
        for file in "$KNOWLEDGE_BASE/client_acquisition/icps"/*.json; do
            if [ -f "$file" ]; then
                echo "<icp_file>$file</icp_file>"
                cat "$file"
            fi
        done
    fi

    # Active Clients
    if [ -d "$KNOWLEDGE_BASE/client_acquisition/clients/active" ]; then
        for file in "$KNOWLEDGE_BASE/client_acquisition/clients/active"/*.json; do
            if [ -f "$file" ]; then
                echo "<client_file>$file</client_file>"
                cat "$file"
            fi
        done
    fi

    # Apollo data
    if [ -d "$KNOWLEDGE_BASE/client_acquisition/apollo" ]; then
        for file in "$KNOWLEDGE_BASE/client_acquisition/apollo"/*.json; do
            if [ -f "$file" ]; then
                echo "<apollo_file>$file</apollo_file>"
                cat "$file"
            fi
        done
    fi

    # Landing pages
    if [ -d "$KNOWLEDGE_BASE/client_acquisition/landing_pages/generated" ]; then
        for file in "$KNOWLEDGE_BASE/client_acquisition/landing_pages/generated"/*.json; do
            if [ -f "$file" ]; then
                echo "<landing_page_file>$file</landing_page_file>"
                cat "$file"
            fi
        done
    fi

    echo "</knowledge_store>"
fi
