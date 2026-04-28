# Contributing to nis2-controls

Thanks for your interest. This library is small on purpose — we want a stable, maintainable mapping rather than a sprawling framework.

## We accept

- ✅ **Mapping corrections** — if we tagged a check with the wrong NIS2 article, open a PR with rationale (cite the article text or BSI guidance).
- ✅ **Mapping additions** — new check → control mappings, especially for ISO 27001 Annex A controls we haven't enriched yet.
- ✅ **Handbook enrichment** — better prose, regulator-source citations, EU translations.
- ✅ **Evidence-type hints** — what auditors typically want to see for each control.
- ✅ **Language helpers** — Python/JS/Rust/Java loaders that wrap the JSON/YAML files.
- ✅ **Schema improvements** — backward-compatible additions to the JSON schema.

## We do not accept

- ❌ Scan engine implementations (commercial scope — see [SaaSFort](https://saasfort.com))
- ❌ Grade computation algorithms (commercial scope)
- ❌ PDF report generators (commercial scope)
- ❌ Mappings to non-NIS2/non-ISO frameworks unless paired with strong demand signal (open an issue first)

## How to submit

1. Fork the repo
2. Create a branch: `git checkout -b fix-control-mapping`
3. Make your change
4. Run CI locally (`make validate`) to ensure JSON/YAML schemas still parse
5. Open a PR with a one-paragraph rationale

## CI

Every PR runs:
- JSON schema validation
- YAML schema validation
- Cross-check that JSON ↔ YAML files are identical content

## Maintainers

- [SaaSFort team](https://saasfort.com) — primary maintenance
- Community contributors welcome
