# Python example — external posture check

Minimal stdlib-only example combining the OSS NIS2 control library in `data/`
with the SaaSFort public report endpoint.

```bash
python external_posture_check.py example.com
```

**What it does:**
1. Loads `data/nis2-controls.json` (the OSS library — the same file you maintain).
2. Calls the free, ungated `GET https://api.saasfort.com/api/report?domain=<target>` endpoint.
3. Prints the externally-observable NIS2 controls so you can wire up report-to-control matching in your own pipeline.

**No dependencies. No signup. No API key.** Just `python 3.x` + an internet connection.

**Cold-cache latency note:** rarely-scanned domains can take 10–20s on the first hit; subsequent hits on the same domain are sub-second.

**Roadmap:** a JSON variant of the report endpoint is planned — open an Issue if you want it sooner. The productionised auditor-formatted PDF + signed-bundle path is the paid one-time audit-pack at [saasfort.com/scan](https://saasfort.com/scan?utm_source=github&utm_medium=oss-example&utm_campaign=nis2-controls-walkthrough). Everything in this folder is OSS and free.

## Contributing
PRs welcome — patterns we'd like next: Go example, JS/TS example, an end-to-end report parser. See `CONTRIBUTING.md` in the repo root.
