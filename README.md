# nis2-controls

A free, open-source NIS2 Article 21 control library for security tooling, GRC platforms, and CI/CD pipelines.

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

## What this is

A machine-readable mapping of **technical security checks → NIS2 Directive Article 21 controls** (and **ISO 27001:2022 Annex A**), extracted from the [SaaSFort](https://saasfort.com) production scan engine.

If you're building a security tool, GRC platform, audit checklist, or CI/CD security gate, you can use this mapping to label every finding with the regulatory control it satisfies — without re-doing the legal research yourself.

## What's included

```
data/
  nis2-controls.json        # NIS2 Article 21 control → checks (machine-readable)
  nis2-controls.yaml        # same, in YAML
  iso27001-mapping.json     # ISO 27001:2022 Annex A control → checks
  iso27001-mapping.yaml     # same, in YAML
HANDBOOK.md                 # human-readable explanation per control + evidence types
```

**Coverage** (auto-generated):

- **9 NIS2 Article 21 controls** mapped (a–j, less §c which is policy-level not technically auto-checkable)
- **12 ISO 27001:2022 Annex A controls** mapped
- **103 unique technical checks** covering TLS, DNS, security headers, OWASP Top 10, certificate transparency, supply chain, and more

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
curl -sL https://raw.githubusercontent.com/saasfort/nis2-controls/main/data/nis2-controls.json -o nis2-controls.json
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
    "https://raw.githubusercontent.com/saasfort/nis2-controls/main/data/nis2-controls.json"))

for ctrl in data["controls"]:
    print(f"{ctrl['control']} — {ctrl['title']}")
    for check in ctrl["checks"]:
        print(f"  • {check}")
```

### Go

```bash
go install github.com/saasfort/nis2-controls/cmd/...@latest
```

```go
import "github.com/saasfort/nis2-controls"
mapping := nis2controls.LoadNIS2()
```

## Schema

```yaml
$schema: https://saasfort.com/schemas/nis2-control-library-v1.json
title: SaaSFort NIS2 Article 21 Control Library
source: NIS2 Directive (EU) 2022/2555 Article 21
generated_at: 2026-04-28T00:00:00Z
license: MIT
repository: https://github.com/saasfort/nis2-controls
controls:
  - control: "NIS2 Art.21(2)(e)"
    title: "Network & information system security..."
    checks: ["DKIM records", "DMARC record", "HSTS", "..."]
    evidence_types: ["Network architecture diagrams", "TLS configuration audits", "..."]
```

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
