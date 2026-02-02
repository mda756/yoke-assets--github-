#!/usr/bin/env python3
"""
Knowledge Store Management Utility
Adds structured data to the Claude Code knowledge repository
"""

import json
import sys
from datetime import datetime
from pathlib import Path

KNOWLEDGE_BASE = Path("claude code creator/knowledge")

def add_icp(data):
    """Add or update an ICP definition"""
    icp_dir = KNOWLEDGE_BASE / "client_acquisition/icps"

    # Validate required fields
    required = ["id", "name", "criteria"]
    for field in required:
        if field not in data:
            return f"Error: Missing required field '{field}'"

    # Add metadata
    if "created_date" not in data:
        data["created_date"] = datetime.now().isoformat()
    if "status" not in data:
        data["status"] = "active"

    # Save
    filename = icp_dir / f"{data['id']}.json"
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)

    return f"ICP saved: {filename}"

def add_client(data):
    """Add or update a client record"""
    status = data.get("status", "prospect")
    folder = "active" if status != "closed_lost" else "archived"
    client_dir = KNOWLEDGE_BASE / f"client_acquisition/clients/{folder}"

    # Validate required fields
    required = ["id", "contact"]
    for field in required:
        if field not in data:
            return f"Error: Missing required field '{field}'"

    # Add metadata
    if "created_date" not in data:
        data["created_date"] = datetime.now().isoformat()

    # Save
    filename = client_dir / f"{data['id']}.json"
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)

    return f"Client saved: {filename}"

def add_landing_page(data):
    """Add landing page metadata"""
    lp_dir = KNOWLEDGE_BASE / "client_acquisition/landing_pages/generated"

    # Validate required fields
    required = ["id", "client_id"]
    for field in required:
        if field not in data:
            return f"Error: Missing required field '{field}'"

    # Add metadata
    if "created_date" not in data:
        data["created_date"] = datetime.now().isoformat()

    # Save
    filename = lp_dir / f"{data['id']}.json"
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)

    return f"Landing page saved: {filename}"

def show_schemas():
    """Display available schemas"""
    schema_file = KNOWLEDGE_BASE / "client_acquisition/_SCHEMAS.json"
    with open(schema_file, 'r') as f:
        schemas = json.load(f)
    return json.dumps(schemas, indent=2)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python add_knowledge.py <type> [json_data]")
        print("Types: icp, client, landing_page, show_schemas")
        print("\nExample:")
        print('  python add_knowledge.py icp \'{"id": "healthcare_saas", "name": "Healthcare SaaS", ...}\'')
        sys.exit(1)

    cmd = sys.argv[1]

    if cmd == "show_schemas":
        print(show_schemas())
        sys.exit(0)

    if len(sys.argv) < 3:
        print("Error: JSON data required")
        sys.exit(1)

    try:
        data = json.loads(sys.argv[2])
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON: {e}")
        sys.exit(1)

    if cmd == "icp":
        print(add_icp(data))
    elif cmd == "client":
        print(add_client(data))
    elif cmd == "landing_page":
        print(add_landing_page(data))
    else:
        print(f"Unknown type: {cmd}")
        sys.exit(1)
