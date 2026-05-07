#!/usr/bin/env python3
"""Validate every data/*.json file against schema/nis2-control-library-v1.json.

Usage (from repo root or anywhere):
    python3 scripts/validate-schema.py

Returns non-zero exit code on any validation failure — suitable for CI.
Requires `jsonschema` (pip install jsonschema). Pinned to Draft 2020-12 to
match the $schema declared in nis2-control-library-v1.json.
"""
import json
import sys
from pathlib import Path
from jsonschema import Draft202012Validator

# Repo root resolves relative to this file so the script is portable for CI.
ROOT = Path(__file__).resolve().parent.parent
SCHEMA_PATH = ROOT / "schema" / "nis2-control-library-v1.json"

with SCHEMA_PATH.open() as f:
    schema = json.load(f)
validator = Draft202012Validator(schema)

failures = 0
for path in sorted((ROOT / "data").glob("*.json")):
    with path.open() as f:
        doc = json.load(f)
    errors = list(validator.iter_errors(doc))
    status = "PASS" if not errors else f"FAIL ({len(errors)} errors)"
    print(f"  {status}  {path.name}")
    for e in errors[:5]:
        print(f"    - {e.message[:140]} (at {'.'.join(map(str, e.absolute_path))})")
    if errors:
        failures += 1

print(f"\n{failures} files failed validation" if failures else "\n✓ All files PASS schema validation")
sys.exit(1 if failures else 0)
