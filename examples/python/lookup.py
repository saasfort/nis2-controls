#!/usr/bin/env python3
"""Look up which compliance controls a security check satisfies, across NIS2,
ISO 27001:2022, BSI IT-Grundschutz and CIS Controls v8.

Usage:
    python3 lookup.py "HSTS"
    python3 lookup.py "DKIM records" --framework nis2
    python3 lookup.py --list-checks
    python3 lookup.py --framework bsi --list-controls

Reads data/check-crosswalk.json from the repo root (relative to this script)
or from the URL when --remote is passed. No third-party dependencies.
"""

import argparse
import json
import sys
import urllib.request
from pathlib import Path

REMOTE_BASE = "https://raw.githubusercontent.com/welcome-archon/nis2-controls/main"
DATA_PATH = Path(__file__).resolve().parents[2] / "data"


def load_json(name: str, remote: bool):
    if remote:
        url = f"{REMOTE_BASE}/data/{name}"
        with urllib.request.urlopen(url) as r:
            return json.loads(r.read().decode("utf-8"))
    with (DATA_PATH / name).open() as f:
        return json.load(f)


def cmd_lookup_check(check_name: str, framework: str | None, remote: bool):
    data = load_json("check-crosswalk.json", remote)
    # Case-insensitive contains match for ergonomics
    needle = check_name.lower()
    matches = [c for c in data["checks"] if needle in c["check"].lower()]
    if not matches:
        print(f"No checks matching {check_name!r}.", file=sys.stderr)
        sys.exit(2)
    for c in matches:
        print(f"\n{c['check']}  → {c['framework_count']} frameworks")
        controls = c["controls"]
        slugs = [framework] if framework else ["nis2", "iso27001", "bsi", "cis-v8", "nist-csf-v2", "dora"]
        for slug in slugs:
            ctrls = controls.get(slug, [])
            if ctrls:
                print(f"  {slug:10s}: {', '.join(ctrls)}")


def cmd_list_checks(remote: bool):
    data = load_json("check-crosswalk.json", remote)
    for c in data["checks"]:
        print(c["check"])


def cmd_list_controls(framework: str, remote: bool):
    fname = {
        "nis2": "nis2-controls.json",
        "iso27001": "iso27001-mapping.json",
        "bsi": "bsi-it-grundschutz-mapping.json",
        "cis-v8": "cis-v8-mapping.json",
        "nist-csf-v2": "nist-csf-v2-mapping.json",
        "dora": "dora-mapping.json",
    }.get(framework)
    if not fname:
        print(f"Unknown framework: {framework}", file=sys.stderr)
        sys.exit(2)
    data = load_json(fname, remote)
    for ctrl in data["controls"]:
        print(f"{ctrl.get('control', '?'):28s}  {ctrl.get('title', '')}")


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("check", nargs="?", help="check name (case-insensitive substring match)")
    ap.add_argument("--framework", choices=["nis2", "iso27001", "bsi", "cis-v8", "nist-csf-v2", "dora"],
                    help="filter / list mode by framework")
    ap.add_argument("--list-checks", action="store_true", help="print all unique check names")
    ap.add_argument("--list-controls", action="store_true",
                    help="print all controls for --framework")
    ap.add_argument("--remote", action="store_true",
                    help="fetch from raw.githubusercontent.com instead of local data/")
    args = ap.parse_args()

    if args.list_checks:
        cmd_list_checks(args.remote)
    elif args.list_controls:
        if not args.framework:
            ap.error("--list-controls requires --framework")
        cmd_list_controls(args.framework, args.remote)
    elif args.check:
        cmd_lookup_check(args.check, args.framework, args.remote)
    else:
        ap.print_help()


if __name__ == "__main__":
    main()
