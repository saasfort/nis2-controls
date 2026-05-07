# Changelog

All notable changes to the SaaSFort NIS2 control library are documented here.
The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and the
project follows semantic versioning.

## [Unreleased]

## [0.7.0] — 2026-05-02

### Added
- `schema/nis2-control-library-v1.json` — JSON Schema (Draft 2020-12) that
  every framework mapping file under `data/` validates against. Locks down the
  contract: required top-level fields ($schema/title/license/repository),
  per-control shape (`control` ID + `checks` array + optional title / category /
  function / implementation_groups / evidence_types), and the dual shape via
  `oneOf` (primary framework files require `controls + source`; the derived
  crosswalk file requires `checks + frameworks`).
- `scripts/validate-schema.py` — CI-ready validator. Run via
  `python3 scripts/validate-schema.py` from the repo root. Returns non-zero
  on any validation failure. Pinned to Draft 2020-12 to match the schema's
  `$schema` declaration. Requires `pip install jsonschema`.
- All 8 existing data files (7 frameworks + crosswalk) re-validated against
  the new schema — 8/8 PASS.

### Why this matters
Before this release, the `"$schema"` URL embedded in every data file was a
placeholder pointing at saasfort.com (which served nothing). Contributors had
no way to validate their own framework PRs locally. The CI lint workflow could
only check JSON parse + YAML parity. With v0.7.0, contributors can:
1. Run the validator before submitting a PR.
2. Get IDE autocomplete + inline hints for the file shape (any IDE that
   reads the `$schema` reference).
3. CI can now reject malformed PRs at the schema layer, not just at the
   YAML/JSON parse layer.

### Repository
- 7 framework files + 1 crosswalk + HANDBOOK + 3 example languages +
  schema + validator + issue/PR templates + lint workflow. Total: 19.

## [0.6.0] — 2026-05-02

### Added
- `data/owasp-asvs-v4-mapping.json` + `.yaml` — OWASP Application Security
  Verification Standard v4.0.3 (Oct 2021), 9 chapters with externally-observable
  Level 1+2 requirements: V2 Authentication, V3 Session Management, V4 Access
  Control, V8 Data Protection, V9 Communications, V10 Malicious Code, V12
  Files & Resources, V13 API & Web Services, V14 Configuration. Skips V1
  (architecture), V5 (input validation), V6 (stored crypto), V7 (error
  handling/logging), V11 (business logic) — they require source review or
  runtime instrumentation, not a public scanner. ASVS published by OWASP
  under CC-BY-SA 4.0; this mapping is independent commentary.
- ASVS is the technical-depth complement to the regulatory frameworks —
  attracts security engineers as a complementary audience to auditors and
  GRC teams.

### Changed
- `data/check-crosswalk.{json,yaml}` regenerated to include `owasp-asvs-v4`.
  103 unique checks: 54 covered in all 7 frameworks (vs 69/6 last release —
  drop reflects ASVS's narrower technical-only scope), 36 in 6, 8 in 5,
  2 in 4, 2 in 3, 1 in 2, 0 in 1.
- All language helpers (Python / JS / Go) updated to surface `owasp-asvs-v4`
  in default output and as a `--framework` choice.
- README expanded: 7-framework coverage row + ASVS in language sample output.

### Repository
- 7 framework files + 1 crosswalk + HANDBOOK + 3 example languages +
  issue/PR templates + lint workflow. Total artefacts: 18.

## [0.5.0] — 2026-05-02

### Added
- `data/dora-mapping.json` + `.yaml` — Digital Operational Resilience Act
  (Regulation (EU) 2022/2554), mandatory for EU financial entities since
  17 January 2026. Covers 7 articles with externally-observable ICT-risk
  management requirements: Art. 7 (ICT systems/protocols/tools), Art. 8
  (asset identification), Art. 9 (protection/prevention/encryption),
  Art. 10 (detection), Art. 13 (vulnerability awareness), Art. 17 (incident
  management contact / disclosure), Art. 28 (third-party JS supply chain).
  Skips Art. 5–6 (governance), 11–16 (response/recovery/learning),
  18–23 (incident reporting/testing), 29–44 (contractual third-party risk)
  — auditors verify those from documentation, not external scans.

### Changed
- `data/check-crosswalk.{json,yaml}` regenerated to include `dora`.
  103 unique checks: 69 covered in all 6 frameworks (vs. 85/5 last release —
  drop reflects DORA's narrower externally-observable scope), 29 in 5,
  1 in 4, 3 in 3, 1 in 2, 0 in 1.
- All language helpers (Python / JS / Go) updated to surface `dora` in
  default output and as a `--framework` choice.
- README expanded: 6-framework coverage row + DORA in language sample
  output.

### Repository
- 6 framework files + 1 crosswalk + HANDBOOK + 3 example languages +
  issue/PR templates + lint workflow. Total artefacts: 17.

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
