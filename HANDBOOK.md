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

## How to use this handbook in an audit

1. Pick the control (e.g. NIS2 Art.21(2)(h) cryptography).
2. Run a scan with any tool that maps to this library (or use [SaaSFort](https://saasfort.com)).
3. Pair scan findings with the evidence-type list to assemble the audit packet.
4. Document deviations explicitly — auditors prefer "we considered X and rejected it for Y" over silence.

## Updates

This handbook tracks the SaaSFort scan engine. As we add new checks (and there are 100+ today), this file is regenerated automatically and PRs are welcome to enrich the handbook prose.

Source repository: https://github.com/saasfort/nis2-controls
Maintained by: [SaaSFort](https://saasfort.com)
