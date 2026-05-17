"""
external_posture_check.py
-------------------------
Minimal example: combine the OSS NIS2 control library in this repo with the
SaaSFort public report endpoint to identify which externally-observable NIS2
controls have evidence for a given domain.

Usage:
    python external_posture_check.py example.com

What it does:
    1. Loads the NIS2 controls JSON from this repo's data/ tree (the OSS
       library — the same file you maintain).
    2. Calls the SaaSFort public report endpoint:
           GET https://api.saasfort.com/api/report?domain=<target>
       This endpoint is free and ungated; it returns an HTML report covering
       ~60 externally-observable checks (TLS, DNS auth, headers, surfaces,
       transparency, etc.).
    3. Prints the NIS2 controls in scope for *external* posture along with the
       OSS-defined external_observable flag, so you can wire up the report-to-
       control matching in your own pipeline.

This script is intentionally read-only and dependency-free (uses only stdlib).

Roadmap note: a JSON variant of the report endpoint is on the SaaSFort roadmap
— if you want it sooner, open an Issue. Today, the productionised path with
PDF + signed-bundle + auditor formatting is the paid one-time audit-pack at
https://saasfort.com/scan?utm_source=github&utm_medium=oss-example&utm_campaign=nis2-controls-walkthrough.
Everything below is OSS and free.
"""
import json
import sys
import urllib.request
from pathlib import Path

REPO_DATA = Path(__file__).resolve().parents[2] / "data" / "nis2-controls.json"
REPORT_API = "https://api.saasfort.com/api/report?domain={domain}"


def load_controls():
    """Load the OSS NIS2 control library from this repo's data/ tree."""
    with REPO_DATA.open("r", encoding="utf-8") as f:
        return json.load(f)


def fetch_report_html(domain: str) -> bytes:
    """Call the free SaaSFort public report endpoint. Returns HTML bytes."""
    url = REPORT_API.format(domain=domain)
    # Cold cache can be 10-20s for rarely-scanned domains; warm cache <1s.
    req = urllib.request.Request(url, headers={"User-Agent": "nis2-controls-example/1.0"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        return resp.read()


def list_external_controls(controls: dict) -> list:
    """Return only controls flagged externally-observable by the OSS schema."""
    out = []
    for c in controls.get("controls", []):
        if c.get("external_observable") is True:
            out.append({
                "id": c.get("id"),
                "title": c.get("title"),
                "article": c.get("article"),
            })
    return out


def main(domain: str) -> int:
    controls = load_controls()
    external = list_external_controls(controls)
    print(f"NIS2 controls flagged externally-observable in OSS library: {len(external)}")
    for c in external:
        print(f"  {c['id']:<10} {c['article']:<20} {c['title']}")
    print()
    print(f"Fetching SaaSFort report for {domain} ...")
    html = fetch_report_html(domain)
    print(f"  -> received {len(html)} bytes of HTML report.")
    print()
    print("Next: parse the report's per-category breakdown and map each finding")
    print("back to the OSS control ids above. The mapping shape is defined in")
    print("data/check-crosswalk.json.")
    return 0


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python external_posture_check.py <domain>", file=sys.stderr)
        sys.exit(2)
    sys.exit(main(sys.argv[1]))
