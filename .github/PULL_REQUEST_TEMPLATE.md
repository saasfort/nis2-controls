<!--
Thanks for the PR. A reviewer will look for these in order:
  1. The change is in scope (see CONTRIBUTING.md — we accept mapping/HANDBOOK/example
     PRs, not scan-engine code or grade algorithms).
  2. Citations are concrete (specific section + page of the underlying standard).
  3. The crosswalk file (data/check-crosswalk.json + .yaml) has been regenerated if any
     framework mapping was modified — this is the artefact consumers query first.
  4. JSON files validate, YAML mirrors are byte-equivalent.
-->

## Summary
<!-- one-paragraph description of what changed and why -->

## Type of change
- [ ] Mapping correction (existing framework)
- [ ] New framework added
- [ ] Example helper / language wrapper
- [ ] HANDBOOK or README improvement
- [ ] Tooling / CI / repo hygiene
- [ ] Other (describe below)

## Citations
<!-- For mapping changes: cite the directive / standard text. Mapping PRs without citations are closed. -->

## Checklist
- [ ] If a `data/*-mapping.json` or `nis2-controls.json` was changed, the YAML mirror was regenerated to match
- [ ] If any framework mapping changed, `data/check-crosswalk.{json,yaml}` was regenerated
- [ ] `examples/` scripts were re-run end-to-end and produce the expected output
- [ ] CHANGELOG.md has an `[Unreleased]` entry describing the change
