# nis2-controls

A free, open-source compliance control library for NIS2, ISO 27001:2022, BSI IT-Grundschutz and CIS Controls v8 — **tied to a working scanner** so every check has a real-world technical signal behind it.

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

## What this is

Machine-readable mappings of **technical security checks → regulatory controls**, extracted from the [SaaSFort](https://saasfort.com) production scan engine.

We ship four mappings out of the box:

- **NIS2 Directive (EU) 2022/2555 Article 21** — 9 controls (a–j, minus §c)
- **ISO 27001:2022 Annex A** — 12 controls
- **BSI IT-Grundschutz Kompendium** (Edition 2023) — 10 modules (Bausteine)
- **CIS Controls v8.1** — 14 controls with IG1/IG2/IG3 implementation groups
- **NIST Cybersecurity Framework v2.0** (Feb 2024) — 9 subcategories with externally-observable signals

If you're building a security tool, GRC platform, audit checklist, or CI/CD security gate, you can use these mappings to label every finding with the regulatory control it satisfies — without redoing the legal research yourself.

## How this is different from other OSS

Several OSS projects offer NIS2 / ISO 27001 / BSI control catalogues — `intuitem/ciso-assistant-community` (130+ frameworks GRC platform), `coolstartnow/isms-builder` (self-hosted ISMS), and BSI's own NIS2-to-ISO/IEC 27001 mapping PDF. They're excellent for policy and gap analysis.

This library is different in three ways:

1. **Tied to a working scanner.** Every mapping entry references a real check name from a production scan engine (60 checks across 21 categories). The mapping isn't aspirational — if a check is in the JSON, the scanner produces a finding for it today.
2. **Four-framework crosswalk in one file.** Most OSS focuses on one or two frameworks. We ship NIS2 + ISO 27001 + BSI IT-Grundschutz + CIS v8 in identical schema so you can crosswalk a single finding to all four with one lookup.
3. **JSON + YAML, optimized for automation.** Designed to drop into CI/CD, GRC platforms, or audit tooling — not just to read.

## What's included

```
data/
  nis2-controls.json                  # NIS2 Article 21 control → checks
  nis2-controls.yaml
  iso27001-mapping.json               # ISO 27001:2022 Annex A control → checks
  iso27001-mapping.yaml
  bsi-it-grundschutz-mapping.json     # BSI IT-Grundschutz Bausteine → checks
  bsi-it-grundschutz-mapping.yaml
  cis-v8-mapping.json                 # CIS Controls v8 (IG1/IG2/IG3) → checks
  cis-v8-mapping.yaml
  nist-csf-v2-mapping.json            # NIST Cybersecurity Framework v2.0 → checks
  nist-csf-v2-mapping.yaml
  check-crosswalk.json                # per-check inverted index across all 5 frameworks
  check-crosswalk.yaml
examples/
  python/lookup.py                    # zero-dependency CLI lookup (Python 3.10+)
  javascript/lookup.js                # zero-dependency CLI lookup (Node 18+)
  go/lookup.go                        # zero-dependency CLI lookup (Go 1.21+)
HANDBOOK.md                           # human-readable explanation per control
CHANGELOG.md                          # release notes
```

**Coverage** (auto-generated):

- **9** NIS2 Article 21 controls
- **12** ISO 27001:2022 Annex A controls
- **10** BSI IT-Grundschutz modules (APP, NET, CON, DER, ORP, OPS)
- **14** CIS Controls v8 controls (IG1–IG3)
- **9** NIST CSF v2.0 subcategories (ID, PR, DE, RS — externally observable only)
- **103 unique technical checks** covering TLS, DNS, security headers, OWASP Top 10, certificate transparency, supply chain, and more
- **85 of 103 checks** map to all five frameworks (true crosswalk coverage)

## One-lookup multi-framework labelling

`data/check-crosswalk.json` is the inverted index. For any check name, you get every control across all four frameworks in one read:

```bash
$ python3 examples/python/lookup.py "HSTS"

HSTS  → 5 frameworks
  nis2       : NIS2 Art.21(2)(e), NIS2 Art.21(2)(h)
  iso27001   : ISO27001 A.8.20, ISO27001 A.8.24
  bsi        : BSI APP.3.2
  cis-v8     : CIS-03
  nist-csf-v2: NIST.PR.DS
```

The same lookup is available in Node (`examples/javascript/lookup.js`) and Go (`examples/go/lookup.go`) — all three produce identical output.

This is the value the README's "four-framework crosswalk in one schema" claim points at — a single lookup gives auditors, GRC platforms, and CI tools the multi-framework label per finding.

## What this is NOT

This repo is **the manual** — the control mapping. It does **not** include:

- A scan engine (commercial — see [saasfort.com](https://saasfort.com))
- A grade computation algorithm
- Auditor-ready PDF report generation
- A multi-domain dashboard
- API/webhook integrations

Use this library to **label** findings from your own scanner. If you want a turnkey NIS2-aware scanner with all of the above, [SaaSFort](https://saasfort.com) starts at €9/month.

## Quick start

### JavaScript / TypeScript

```bash
curl -sL https://raw.githubusercontent.com/welcome-archon/nis2-controls/main/data/nis2-controls.json -o nis2-controls.json
```

```js
import controls from './nis2-controls.json' assert { type: 'json' };

// Find which NIS2 article a check satisfies
const article = controls.controls.find(c => c.checks.includes('HSTS'));
console.log(article.control); // "NIS2 Art.21(2)(e)"
console.log(article.title);   // "Network & information system security..."
```

### Python

```python
import json, urllib.request
data = json.load(urllib.request.urlopen(
    "https://raw.githubusercontent.com/welcome-archon/nis2-controls/main/data/nis2-controls.json"))

for ctrl in data["controls"]:
    print(f"{ctrl['control']} — {ctrl['title']}")
    for check in ctrl["checks"]:
        print(f"  • {check}")
```

### Go

```bash
go install github.com/welcome-archon/nis2-controls/cmd/...@latest
```

```go
import "github.com/welcome-archon/nis2-controls"
mapping := nis2controls.LoadNIS2()
```

## Schema

```yaml
$schema: https://saasfort.com/schemas/nis2-control-library-v1.json
title: SaaSFort NIS2 Article 21 Control Library
source: NIS2 Directive (EU) 2022/2555 Article 21
generated_at: 2026-04-28T00:00:00Z
license: MIT
repository: https://github.com/welcome-archon/nis2-controls
controls:
  - control: "NIS2 Art.21(2)(e)"
    title: "Network & information system security..."
    checks: ["DKIM records", "DMARC record", "HSTS", "..."]
    evidence_types: ["Network architecture diagrams", "TLS configuration audits", "..."]
```

## Live API mirror

The same mapping data is also served from the SaaSFort API for clients that prefer HTTP over a git checkout. Useful for in-product pickers, CI/CD steps, and read-only integrations.

```
GET https://api.saasfort.com/api/nis2/controls
GET https://api.saasfort.com/api/nis2/controls/nis2
GET https://api.saasfort.com/api/nis2/controls/iso27001
GET https://api.saasfort.com/api/nis2/controls/bsi
GET https://api.saasfort.com/api/nis2/controls/cis-v8
```

Response is identical to the JSON files in `data/`. CORS is wide-open (`Access-Control-Allow-Origin: *`) and responses are cached for one hour.

## Contributing

We accept PRs that:

- ✅ Add or correct check → control mappings
- ✅ Improve the human-readable HANDBOOK
- ✅ Add language-specific helpers (Python/JS/Rust/etc.)
- ✅ Add or refine evidence-type hints
- ✅ Translate the HANDBOOK to other EU languages

We **do not** accept PRs that:

- ❌ Add scan engine implementation (out of scope — that's commercial)
- ❌ Add grade computation algorithms (out of scope)
- ❌ Add auditor-grade report generators (out of scope)

See [CONTRIBUTING.md](CONTRIBUTING.md) for details.

## Why we open-sourced this

The control mapping is the *manual*. Sharing it is good for the EU security ecosystem and good for SaaSFort:

- **Auditors** get a free reference they can vet
- **GRC platforms** can integrate without us
- **CI tools** can label findings without us
- **Procurement teams** get a consistent vocabulary

What stays paid is the **scanner** that produces the findings, the **grade** that summarizes posture, and the **auditor-ready PDF report** that makes a CISO's life easier. That's where SaaSFort earns its €9–29/month.

This is the [HashiCorp / Ansible / OWASP](https://en.wikipedia.org/wiki/Open-source_software_business_model#Open_core) playbook applied to compliance tooling.

## License

MIT — see [LICENSE](LICENSE).

The mapping data is published under MIT. The NIS2 Directive itself is © European Union and reproduced for educational purposes under fair-use principles.

## Maintained by

[SaaSFort](https://saasfort.com) — external security posture scanner with NIS2/ISO 27001 compliance reports. Try a free scan: [saasfort.com/scan](https://saasfort.com/scan).
