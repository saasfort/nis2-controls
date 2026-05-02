#!/usr/bin/env node
/**
 * Look up which compliance controls a security check satisfies, across NIS2,
 * ISO 27001:2022, BSI IT-Grundschutz and CIS Controls v8.
 *
 * Usage:
 *   node lookup.js "HSTS"
 *   node lookup.js "DKIM records" --framework nis2
 *   node lookup.js --list-checks
 *   node lookup.js --framework bsi --list-controls
 *
 * Reads data/check-crosswalk.json from the repo (relative to this script)
 * or from the URL when --remote is passed. Zero npm dependencies — Node 18+
 * (uses global fetch).
 */

const fs = require("node:fs");
const path = require("node:path");

const REMOTE_BASE = "https://raw.githubusercontent.com/welcome-archon/nis2-controls/main";
const DATA_PATH = path.resolve(__dirname, "..", "..", "data");

async function loadJson(name, remote) {
  if (remote) {
    const r = await fetch(`${REMOTE_BASE}/data/${name}`);
    if (!r.ok) throw new Error(`fetch ${name}: ${r.status}`);
    return r.json();
  }
  return JSON.parse(fs.readFileSync(path.join(DATA_PATH, name), "utf8"));
}

function parseArgs(argv) {
  const args = { check: null, framework: null, listChecks: false, listControls: false, remote: false };
  for (let i = 2; i < argv.length; i++) {
    const a = argv[i];
    if (a === "--framework") args.framework = argv[++i];
    else if (a === "--list-checks") args.listChecks = true;
    else if (a === "--list-controls") args.listControls = true;
    else if (a === "--remote") args.remote = true;
    else if (a === "-h" || a === "--help") return null;
    else if (!a.startsWith("--")) args.check = a;
  }
  return args;
}

function help() {
  console.log("Usage: node lookup.js <check-name> [--framework nis2|iso27001|bsi|cis-v8] [--remote]");
  console.log("       node lookup.js --list-checks [--remote]");
  console.log("       node lookup.js --framework <name> --list-controls [--remote]");
}

async function lookupCheck(checkName, framework, remote) {
  const data = await loadJson("check-crosswalk.json", remote);
  const needle = checkName.toLowerCase();
  const matches = data.checks.filter((c) => c.check.toLowerCase().includes(needle));
  if (matches.length === 0) {
    console.error(`No checks matching ${JSON.stringify(checkName)}.`);
    process.exit(2);
  }
  const slugs = framework ? [framework] : ["nis2", "iso27001", "bsi", "cis-v8"];
  for (const c of matches) {
    console.log(`\n${c.check}  → ${c.framework_count} frameworks`);
    for (const s of slugs) {
      const ctrls = c.controls[s] || [];
      if (ctrls.length) console.log(`  ${s.padEnd(10)}: ${ctrls.join(", ")}`);
    }
  }
}

async function listChecks(remote) {
  const data = await loadJson("check-crosswalk.json", remote);
  data.checks.forEach((c) => console.log(c.check));
}

async function listControls(framework, remote) {
  const fname = {
    nis2: "nis2-controls.json",
    iso27001: "iso27001-mapping.json",
    bsi: "bsi-it-grundschutz-mapping.json",
    "cis-v8": "cis-v8-mapping.json",
  }[framework];
  if (!fname) {
    console.error(`Unknown framework: ${framework}`);
    process.exit(2);
  }
  const data = await loadJson(fname, remote);
  data.controls.forEach((c) => {
    console.log(`${(c.control || "?").padEnd(28)}  ${c.title || ""}`);
  });
}

(async () => {
  const args = parseArgs(process.argv);
  if (!args) return help();
  if (args.listChecks) return listChecks(args.remote);
  if (args.listControls) {
    if (!args.framework) { help(); process.exit(2); }
    return listControls(args.framework, args.remote);
  }
  if (args.check) return lookupCheck(args.check, args.framework, args.remote);
  help();
})().catch((e) => { console.error(e.message); process.exit(1); });
