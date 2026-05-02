# Changelog

All notable changes to the SaaSFort NIS2 control library are documented here.
The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and the
project follows semantic versioning.

## [Unreleased]

## [0.4.0] — 2026-05-02

### Added
- `data/nist-csf-v2-mapping.json` + `.yaml` — NIST Cybersecurity Framework v2.0
  (released Feb 2024). 9 subcategories across the 6 v2 functions
  (Identify / Protect / Detect / Respond) with externally-observable signals.
  Skips Govern (GV.*), Recover (RC.*) and pure governance subcategories — no
  external scanner can verify them.
- `examples/go/lookup.go` — zero-dependency Go CLI lookup tool, completes the
  language trio (Python + JS + Go). Standard library only, supports `-remote`.
- `.github/ISSUE_TEMPLATE/mapping_correction.yml` — structured intake for
  check↔control changes; requires citation.
- `.github/ISSUE_TEMPLATE/new_framework.yml` — gates new-framework requests
  on (a) at least one externally-observable subcategory, (b) public source.
- `.github/PULL_REQUEST_TEMPLATE.md` — reviewer checklist incl. crosswalk
  regeneration + YAML/JSON parity.
- README updated: 5-framework coverage row + NIST CSF v2 sample lookup output.

### Changed
- `data/check-crosswalk.{json,yaml}` regenerated to include `nist-csf-v2`.
  103 unique checks: 85 covered in all 5 frameworks (vs. 85/4 last release),
  14 in 4 frameworks, 3 in 3, 1 in 2, 0 in 1.
- All language helpers (Python / JS / Go) updated to surface `nist-csf-v2` in
  default output and as a `--framework` choice.

### Repository
- 5 framework files + 1 crosswalk + HANDBOOK + 3 example languages +
  issue/PR templates. Total artefacts: 16.

## [0.3.0] — 2026-05-02

### Added
- `data/check-crosswalk.json` + `.yaml` — inverted index per check name to every
  control across all four frameworks. 103 unique checks; 85 covered in all four
  frameworks. Single lookup gives a finding's multi-framework label.
- `examples/python/lookup.py` — zero-dependency CLI lookup tool against the local
  data/ files or `--remote` GitHub raw mirror.
- `examples/javascript/lookup.js` — same in Node 18+ (uses global fetch).
- `CHANGELOG.md` — this file.

## [0.2.0] — 2026-05-02

### Added
- `data/bsi-it-grundschutz-mapping.json` + `.yaml` — 10 BSI Bausteine (APP.3.1,
  APP.3.2, APP.5.1, CON.1, CON.10, DER.1, NET.1.1, OPS.1.1.3, OPS.1.2.6, ORP.4)
  covering externally-observable requirements only.
- `data/cis-v8-mapping.json` + `.yaml` — 14 CIS Controls v8 controls with IG1/IG2/IG3
  implementation groups. Skips CIS-08/10/11/14 because no external scanner can
  verify audit logs / malware defences / backups / training.
- README expanded: three differentiators vs adjacent OSS (intuitem/ciso-assistant-community,
  isms-builder, BSI's own NIS2-ISO PDF) — scanner-tied, four-framework crosswalk in
  one schema, JSON+YAML for automation.
- HANDBOOK.md extended with BSI module table + CIS control table.
- Live API mirror documented at https://api.saasfort.com/api/nis2/controls.

## [0.1.0] — 2026-04-28

### Added
- Initial release: `data/nis2-controls.json` + `.yaml` (9 NIS2 Article 21 controls,
  a–j minus §c) and `data/iso27001-mapping.json` + `.yaml` (12 ISO 27001:2022
  Annex A controls).
- HANDBOOK.md, README.md, CONTRIBUTING.md, LICENSE (MIT).
- 103 unique technical checks covering TLS, DNS, security headers, OWASP Top 10,
  certificate transparency, supply chain.
