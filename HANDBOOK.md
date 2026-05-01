# NIS2 Article 21 Control Handbook

A human-readable companion to `data/nis2-controls.json`. For each control under Article 21(2) of the NIS2 Directive ((EU) 2022/2555), this handbook explains:

- What the regulator expects
- Which technical checks satisfy it (mapped from the SaaSFort scan engine)
- What evidence types an auditor will likely want

This is the *manual* — extracted from a production scanner so the mapping is grounded in real checks, not abstract policy text.

---

## NIS2 Art.21(2)(a) — Risk analysis & information system security policies

**What the regulator wants**: A documented, regularly-reviewed risk-management process covering all information systems in scope.

**Technical checks (proxy signals)**:
- SPF record present and well-formed
- DMARC record published with quarantine/reject policy
- CAA record limits which CAs can issue for your domain
- Subdomain enumeration shows you have a current asset inventory
- DKIM records aligned with sending domains

**Evidence types**:
- Risk register (annually reviewed)
- Threat model document
- Annual risk review minutes signed by management

---

## NIS2 Art.21(2)(b) — Incident handling

**What the regulator wants**: Documented procedures for detection, reporting, response, and post-mortem of security incidents.

**Technical checks**:
- `security.txt` (RFC 9116) — provides a contact channel for vulnerability reports
- `.git` directory not exposed (would reveal source disclosure incidents)
- No sensitive files (`.env`, `.bak`, etc.) accessible

**Evidence types**:
- Incident response runbook
- Post-incident review reports for last 3 incidents
- Notification log (who was notified, when, by what means)

---

## NIS2 Art.21(2)(c) — Business continuity & crisis management

**What the regulator wants**: Backup, recovery, and crisis comms procedures with tested RTO/RPO targets.

**Technical checks (limited — this is mostly policy)**:
- DNS resilience signals (multiple nameservers, distinct AS numbers)
- HTTP/2 support (graceful degradation)

**Evidence types**:
- Business Continuity Plan / Disaster Recovery Plan
- Backup test results (last 12 months)
- Defined RTO and RPO targets with sign-off

---

## NIS2 Art.21(2)(d) — Supply chain security

**What the regulator wants**: Security assessment of suppliers, including subprocessors and SaaS dependencies.

**Technical checks**:
- Subresource Integrity (SRI) on third-party scripts
- CORS policy not overly permissive
- JavaScript library vulnerability scan (no known-vulnerable versions)
- Source map exposure check (don't leak proprietary code)

**Evidence types**:
- Supplier security questionnaires
- Data Processing Agreements
- Subprocessor list with security tier

---

## NIS2 Art.21(2)(e) — Network & information system security

**What the regulator wants**: Secure acquisition, development, and maintenance of systems — including secure configuration of production endpoints.

**Technical checks**:
- HTTPS-only (HTTP redirects to HTTPS)
- HSTS with sufficient `max-age` and `includeSubDomains`
- HSTS preload (where appropriate)
- TLS 1.2 minimum (no TLS 1.0 / 1.1)
- DNSSEC enabled
- WAF/CDN detected
- Stale subdomain detection (no orphaned subdomains pointing at retired services)

**Evidence types**:
- Network architecture diagrams (current)
- TLS configuration audit screenshots
- DNS health monitoring exports

---

## NIS2 Art.21(2)(f) — Effectiveness assessment

**What the regulator wants**: Procedures to test whether your security measures actually work — pen tests, vuln scans, red-team exercises.

**Technical checks**:
- SQL injection patterns (basic detection)
- Reflected XSS reflection
- Open redirect
- Directory listing
- `.git` exposure
- Sensitive file exposure
- Dangerous HTTP methods enabled
- Source map exposure
- Rate limiting present

**Evidence types**:
- External vulnerability scan reports
- Penetration test reports (annual)
- Patch management policy + last 3 months patch evidence

---

## NIS2 Art.21(2)(g) — Cyber hygiene & training

**What the regulator wants**: Basic security hygiene practices — strong configurations, security headers, awareness training for staff.

**Technical checks**:
- Content Security Policy (CSP) present, strong, and reporting enabled
- `object-src 'none'`
- `base-uri` restricted
- X-Frame-Options or CSP frame-ancestors (clickjacking)
- X-Content-Type-Options: nosniff
- Referrer-Policy strict
- Permissions-Policy locks down sensors
- Server header doesn't disclose version
- X-Powered-By absent
- Cross-Origin headers (COOP/COEP/CORP)
- Cache-Control on sensitive responses
- Robots.txt doesn't leak sensitive paths

**Evidence types**:
- Security training records (LMS exports)
- Awareness campaign materials
- Phishing test results

---

## NIS2 Art.21(2)(h) — Cryptography & encryption

**What the regulator wants**: Documented cryptography policy — when to encrypt, what algorithms, certificate lifecycle, key management.

**Technical checks**:
- Valid certificate (not expired, not self-signed in prod)
- Strong key size (RSA ≥ 2048, ECDSA ≥ 256)
- Strong signature algorithm (no SHA-1)
- Strong cipher suites
- TLS 1.3 supported
- TLS session resumption configured
- OCSP stapling
- Certificate Transparency (CT) log presence
- CA diversity (don't depend on a single CA)
- Recent certificate issuance pattern healthy
- HPKP / Expect-CT not present (deprecated)
- Insecure form actions absent

**Evidence types**:
- Cryptography policy document
- Cipher inventory across all production endpoints
- Certificate lifecycle records (issuance, renewal, revocation)

---

## NIS2 Art.21(2)(i) — Access control & asset management

**What the regulator wants**: RBAC, asset inventory, regular access reviews.

**Technical checks**:
- Cookie security (`Secure`, `HttpOnly`, `SameSite`)
- Cookie prefix security (`__Secure-`, `__Host-`)
- Admin panel exposure (no admin URLs reachable from public internet)
- CORS credential reflection (no `*` with credentials)
- Clear-Site-Data on logout

**Evidence types**:
- Access review reports (last 12 months)
- RBAC matrix
- Asset inventory (current)

---

## NIS2 Art.21(2)(j) — MFA & secured comms

**What the regulator wants**: Multi-factor authentication for privileged access; secured voice/video/text comms; secure emergency comms.

**Technical checks**:
- Cookie security supports session integrity
- `.well-known/change-password` exposed (RFC 8615) so password managers can drive flow
- Clear-Site-Data on logout

**Evidence types**:
- MFA enforcement policy + screenshot of admin tooling configuration
- Secure comms inventory (Signal, Wire, etc.)
- Emergency comms procedure (out-of-band channel)

---

---

## BSI IT-Grundschutz baseline mapping

The German BSI IT-Grundschutz Kompendium structures controls as **Bausteine** (modules) — APP for applications, NET for networks, CON for concepts, ORP for organisation/personnel, OPS for operations, DER for detection. We map only the modules whose requirements have an externally observable component:

| Module | Title | Externally observable? |
|---|---|---|
| APP.3.1 | Web applications | Partially — XSS, SQLi, exposure |
| APP.3.2 | Web servers | Yes — security headers, TLS |
| APP.5.1 | General e-mail | Yes — SPF, DKIM, DMARC, MX |
| CON.1 | Cryptographic concept | Yes — TLS, certificates, ciphers |
| CON.10 | Web application development | Yes — CSP, CORS, SRI, JS libs |
| DER.1 | Detection of security events | Partially — WAF, rate limiting |
| NET.1.1 | Network architecture & design | Yes — DNS, subdomains, DNSSEC |
| OPS.1.1.3 | Patch & change management | Partially — deprecated headers, lib versions |
| OPS.1.2.6 | Incident response | Partially — security.txt, exposure tells |
| ORP.4 | Identity & access management | Partially — admin panels, cookies |

For each module, `data/bsi-it-grundschutz-mapping.json` lists the SaaSFort checks that contribute evidence and the auditor-facing evidence types that pair with the technical signal. Modules covering pure organisational, physical or procedural controls (e.g. ISMS.1, ORP.1, INF.*) are intentionally absent — no external scanner can verify them.

Authoritative reference: BSI IT-Grundschutz Kompendium ([bsi.bund.de/grundschutz](https://www.bsi.bund.de/dok/IT-Grundschutz-Kompendium-en)).

---

## CIS Controls v8 mapping

The Center for Internet Security publishes 18 top-level controls and 153 safeguards, grouped into Implementation Groups (IG1 / IG2 / IG3) by maturity. We map only the controls with at least one externally-observable safeguard:

| Control | Title | Why externally observable |
|---|---|---|
| CIS-01 | Inventory & control of enterprise assets | DNS, CT logs, subdomain enumeration |
| CIS-02 | Inventory & control of software assets | JS libraries, server header fingerprints |
| CIS-03 | Data protection | HSTS, TLS configuration, encryption-in-transit |
| CIS-04 | Secure configuration | Security headers, error pages |
| CIS-05 | Account management | Cookie security, admin panel exposure |
| CIS-06 | Access control management | CORS, rate limiting, admin panels |
| CIS-07 | Continuous vulnerability management | Lib vulnerabilities, exposure, deprecated headers |
| CIS-09 | Email & web browser protections | SPF, DKIM, DMARC, MX |
| CIS-12 | Network infrastructure management | DNSSEC, nameservers, CAA |
| CIS-13 | Network monitoring & defense | WAF/CDN, rate limiting |
| CIS-15 | Service provider management | Third-party JS, SRI, CA diversity |
| CIS-16 | Application software security | CSP, CORS, OWASP Top 10 signals |
| CIS-17 | Incident response management | security.txt |
| CIS-18 | Penetration testing | Reachability of admin/dev paths |

CIS-08 (Audit Logs), CIS-10 (Malware Defenses), CIS-11 (Data Recovery) and CIS-14 (Security Awareness) are intentionally absent: no public-facing scan can verify whether an organisation logs its events, runs EDR, tests its backups or trains its staff. They remain the auditor's job, not the scanner's.

Authoritative reference: CIS Critical Security Controls v8.1 ([cisecurity.org/controls](https://www.cisecurity.org/controls)).

---

## How to use this handbook in an audit

1. Pick the control (e.g. NIS2 Art.21(2)(h) cryptography, BSI CON.1, or CIS-03).
2. Run a scan with any tool that maps to this library (or use [SaaSFort](https://saasfort.com)).
3. Pair scan findings with the evidence-type list to assemble the audit packet.
4. Document deviations explicitly — auditors prefer "we considered X and rejected it for Y" over silence.

## Updates

This handbook tracks the SaaSFort scan engine. As we add new checks (and there are 100+ today), this file is regenerated automatically and PRs are welcome to enrich the handbook prose.

Source repository: https://github.com/welcome-archon/nis2-controls
Maintained by: [SaaSFort](https://saasfort.com)
