#!/usr/bin/env python3
"""
generate_security_checklist.py — Generates a personalised Markdown security
checklist based on project type and authentication mechanism.

Usage:
    python3 generate_security_checklist.py --type api --auth jwt --output security-checklist.md
    python3 generate_security_checklist.py --type webapp --auth session --output checklist.md
    python3 generate_security_checklist.py --type mobile --auth oauth2 --output mobile-security.md
    python3 generate_security_checklist.py --type microservices --auth apikey --output ms-checklist.md
"""

import argparse
import sys
from datetime import datetime

# ---------------------------------------------------------------------------
# Section 1 — Authentication (varies by auth mechanism)
# ---------------------------------------------------------------------------

AUTH_CHECKS: dict[str, list[str]] = {
    "jwt": [
        "[ ] Validate the `alg` header — reject `none` and unexpected algorithms (use RS256 or ES256, avoid HS256 for distributed systems)",
        "[ ] Verify `exp` (expiration) claim on every request; reject expired tokens immediately",
        "[ ] Verify `nbf` (not before) claim to prevent premature token use",
        "[ ] Verify `aud` (audience) claim to prevent token misuse across services",
        "[ ] Verify `iss` (issuer) claim against a whitelist of trusted issuers",
        "[ ] Keep access token TTL short (5–15 min); use refresh tokens for session continuity",
        "[ ] Implement refresh token rotation (each use issues a new token, old one is invalidated)",
        "[ ] Detect and block refresh token reuse — flag as potential token theft, revoke the entire family",
        "[ ] Store JWTs in HttpOnly, Secure, SameSite=Strict cookies (never in localStorage for sensitive apps)",
        "[ ] Implement a token revocation mechanism (blocklist, short TTL, or OIDC logout endpoint)",
        "[ ] Rotate JWT signing keys regularly; support key ID (`kid`) for zero-downtime rotation",
        "[ ] Never expose sensitive PII (passwords, card numbers, raw secrets) in JWT payload — it is base64-encoded, not encrypted",
    ],
    "oauth2": [
        "[ ] Use Authorization Code flow with PKCE for all public clients (SPA, mobile)",
        "[ ] Whitelist redirect_uri values strictly — no wildcard patterns",
        "[ ] Generate a cryptographically random `state` parameter; validate it on callback to prevent CSRF",
        "[ ] Use PKCE `code_verifier` / `code_challenge` (S256 method) for every authorization request",
        "[ ] Request only the minimum OAuth scopes needed (principle of least privilege)",
        "[ ] Validate access tokens on every API call; do not cache validation results beyond token TTL",
        "[ ] Implement token introspection or JWKS-based local validation depending on token type",
        "[ ] Rotate refresh tokens on each use; enforce absolute expiry (e.g., 30 days)",
        "[ ] Implement logout that revokes both access and refresh tokens at the authorization server",
        "[ ] Use the BFF (Backend-For-Frontend) pattern for SPAs to keep tokens server-side",
        "[ ] Enforce mTLS or DPoP for high-security token binding (prevents token replay attacks)",
        "[ ] Monitor for suspicious OAuth patterns: repeated token requests, unusual scope escalation",
    ],
    "session": [
        "[ ] Generate session IDs using a cryptographically secure random source (min. 128 bits of entropy)",
        "[ ] Set cookies with `HttpOnly`, `Secure`, and `SameSite=Strict` (or `Lax` minimum) flags",
        "[ ] Regenerate session ID immediately after authentication (prevents session fixation)",
        "[ ] Invalidate server-side session data on logout (do not rely on cookie deletion alone)",
        "[ ] Implement absolute session timeout (e.g., 8 hours) and idle session timeout (e.g., 30 min)",
        "[ ] Implement CSRF tokens for every state-changing request (synchronizer token pattern)",
        "[ ] Consider Double Submit Cookie pattern as a stateless CSRF mitigation for APIs",
        "[ ] Protect session store (Redis, DB) with authentication and network isolation",
        "[ ] Limit concurrent sessions per user if required by the security policy",
        "[ ] Log all session lifecycle events: creation, renewal, expiry, forced invalidation",
        "[ ] Use `__Host-` cookie prefix for maximum security when applicable",
        "[ ] Never expose the session ID in URLs, logs, or error messages",
    ],
    "apikey": [
        "[ ] Generate API keys using a cryptographically secure random source (min. 256 bits)",
        "[ ] Store only a hashed version of the API key (bcrypt or Argon2) — never the plaintext",
        "[ ] Scope API keys to specific permissions / resources; avoid all-access keys",
        "[ ] Enforce mandatory key expiry dates; provide key rotation UI/API for clients",
        "[ ] Implement per-key rate limiting to prevent abuse and detect compromised keys",
        "[ ] Transmit API keys via `Authorization: Bearer <key>` header only — never in query strings",
        "[ ] Rotate keys without downtime: support grace period where old and new key are both valid",
        "[ ] Provide immediate key revocation capability (self-service + admin override)",
        "[ ] Alert on unusual usage patterns: new IP, abnormal request volume, off-hours access",
        "[ ] Log all API key usage with timestamp, IP, and endpoint for audit trail",
        "[ ] Implement key prefixing (e.g., `sk_live_...`) to facilitate secret scanning in code repos",
        "[ ] Integrate secret scanning in CI/CD (GitGuardian, TruffleHog) to detect accidental commits",
    ],
}

# ---------------------------------------------------------------------------
# Section 2 — Authorization
# ---------------------------------------------------------------------------

AUTHORIZATION_CHECKS: list[str] = [
    "[ ] Define and document the authorization model (RBAC, ABAC, ReBAC, or combination)",
    "[ ] Apply the principle of least privilege at every layer: API gateway, service, database",
    "[ ] Enforce resource-level access checks — verify ownership/permission on every object, not just endpoint",
    "[ ] Centralize authorization logic in a dedicated middleware or policy engine (avoid scattered `if role == ...`)",
    "[ ] Test authorization rules with unit tests covering both positive and negative cases",
    "[ ] Audit privilege escalation paths — ensure no role can grant itself higher permissions",
    "[ ] Implement Row-Level Security (RLS) at the database layer for multi-tenant data isolation",
    "[ ] Review and prune permissions regularly — remove access that is no longer needed",
    "[ ] Log all authorization decisions for sensitive actions (access granted and denied)",
    "[ ] Consider a policy engine (OPA, Cedar, Casbin) for complex or microservice authorization",
]

# ---------------------------------------------------------------------------
# Section 3 — Data Protection
# ---------------------------------------------------------------------------

DATA_PROTECTION_CHECKS: list[str] = [
    "[ ] Enforce HTTPS everywhere with HSTS (`Strict-Transport-Security: max-age=31536000; includeSubDomains; preload`)",
    "[ ] Use TLS 1.2 minimum; prefer TLS 1.3; disable TLS 1.0 and 1.1",
    "[ ] Store all secrets in a dedicated secret manager (HashiCorp Vault, AWS Secrets Manager, GCP Secret Manager)",
    "[ ] Never hardcode secrets, credentials, or API keys in source code or config files",
    "[ ] Enable secret scanning in CI/CD pipelines (GitGuardian, TruffleHog, GitHub Advanced Security)",
    "[ ] Encrypt sensitive data at rest (AES-256 or equivalent); manage encryption keys separately from data",
    "[ ] Implement PII data minimization — collect only what is strictly necessary for the business purpose",
    "[ ] Define and enforce data retention policies; automate deletion of expired data",
    "[ ] Anonymize or pseudonymize PII in non-production environments (dev, staging, test)",
    "[ ] Redact sensitive fields (passwords, tokens, card numbers, SSNs) from all logs automatically",
    "[ ] Rotate all credentials and secrets on a schedule (max TTL: 90 days for standard, 24h for high sensitivity)",
    "[ ] Audit access to sensitive data stores with immutable audit logs",
]

# ---------------------------------------------------------------------------
# Section 4 — Input Validation (varies by project type)
# ---------------------------------------------------------------------------

BASE_INPUT_CHECKS: list[str] = [
    "[ ] Validate all inputs server-side regardless of client-side validation",
    "[ ] Use allow-lists (whitelist) rather than deny-lists (blacklist) for input validation",
    "[ ] Sanitize and escape all output to the appropriate context (HTML, SQL, JSON, shell)",
    "[ ] Use parameterized queries / prepared statements — never build SQL from string concatenation (SQLi)",
    "[ ] Validate content types and reject unexpected MIME types",
    "[ ] Enforce maximum input sizes to prevent buffer overflows and DoS via large payloads",
    "[ ] Validate file uploads: type, size, filename (no path traversal), scan for malware if possible",
]

EXTRA_INPUT_CHECKS: dict[str, list[str]] = {
    "webapp": [
        "[ ] Escape all HTML output (XSS prevention) — use auto-escaping templating engines",
        "[ ] Implement Content Security Policy (CSP) to restrict script sources",
        "[ ] Add `X-Content-Type-Options: nosniff` to prevent MIME sniffing",
        "[ ] Protect forms with CSRF tokens (synchronizer token or double-submit cookie)",
        "[ ] Validate and sanitize rich text / markdown input with an allow-list HTML sanitizer",
        "[ ] Use `rel='noopener noreferrer'` on all external links opened in new tabs",
    ],
    "api": [
        "[ ] Validate request payloads against a strict JSON schema before processing",
        "[ ] Reject requests with unexpected extra fields (prevent mass-assignment vulnerabilities)",
        "[ ] Implement CORS with an explicit origin whitelist — never use `*` for authenticated endpoints",
        "[ ] Validate path parameters, query strings, and headers — not just request bodies",
        "[ ] Return 400 with a generic error for validation failures — never echo back raw input in errors",
    ],
    "mobile": [
        "[ ] Validate all data received from the API client-side before rendering",
        "[ ] Implement certificate pinning to prevent MITM attacks",
        "[ ] Sanitize data stored locally (SQLite, files) to prevent local injection attacks",
        "[ ] Do not log sensitive data to the device console or crash reporters",
        "[ ] Validate deep-link URLs and intent parameters before processing",
    ],
    "microservices": [
        "[ ] Validate all inter-service messages/events against a schema (Protobuf, Avro, JSON Schema)",
        "[ ] Do not trust service-to-service calls implicitly — verify JWT or mTLS on each hop",
        "[ ] Validate and sanitize data from message queues as if from untrusted sources",
        "[ ] Implement circuit breakers to handle malformed or unexpected data from downstream services",
        "[ ] Validate external webhook payloads using HMAC signatures before processing",
    ],
}

# ---------------------------------------------------------------------------
# Section 5 — Infrastructure & Headers
# ---------------------------------------------------------------------------

INFRA_CHECKS: list[str] = [
    "[ ] Set `Content-Security-Policy` header to restrict allowed sources for scripts, styles, and frames",
    "[ ] Set `X-Content-Type-Options: nosniff` on all responses",
    "[ ] Set `X-Frame-Options: DENY` (or use CSP `frame-ancestors 'none'`) to prevent clickjacking",
    "[ ] Set `Referrer-Policy: strict-origin-when-cross-origin` to limit referrer leakage",
    "[ ] Set `Permissions-Policy` to disable unused browser features (camera, microphone, geolocation)",
    "[ ] Remove `Server`, `X-Powered-By`, and other version-revealing headers",
    "[ ] Configure CORS with an explicit allow-list — deny by default",
    "[ ] Implement rate limiting at the API gateway or middleware layer (per IP, per user, per key)",
    "[ ] Implement request throttling and DDoS protection (Cloudflare, AWS Shield, or equivalent)",
    "[ ] Enable and review Web Application Firewall (WAF) rules for your traffic patterns",
    "[ ] Emit structured security audit logs: who, what, when, from where, outcome",
    "[ ] Set up alerting for security events: repeated auth failures, privilege escalation, unusual traffic",
    "[ ] Automate dependency vulnerability scanning in CI/CD (Snyk, Dependabot, OWASP Dependency-Check)",
    "[ ] Pin or lock dependency versions; review updates before applying in production",
]

# ---------------------------------------------------------------------------
# Section 6 — Incident Response
# ---------------------------------------------------------------------------

INCIDENT_RESPONSE_CHECKS: list[str] = [
    "[ ] Define a documented security incident response plan with clear roles and escalation paths",
    "[ ] Implement breach detection: anomaly alerts on auth failures, data exfiltration patterns, unusual API usage",
    "[ ] Ensure immediate token/session/key revocation capability (< 5 min from detection to revocation)",
    "[ ] Implement user notification process for security incidents affecting their data",
    "[ ] Maintain an immutable audit log that cannot be altered by compromised application credentials",
    "[ ] Define RTO/RPO for security incidents; test recovery procedures regularly",
    "[ ] Practice tabletop exercises or breach simulation at least quarterly",
    "[ ] Have a coordinated disclosure (responsible disclosure) process for external reporters",
    "[ ] Conduct post-mortem for every security incident; track remediation action items to completion",
    "[ ] Keep an up-to-date asset inventory and data flow diagram to accelerate incident scoping",
]

# ---------------------------------------------------------------------------
# Document builder
# ---------------------------------------------------------------------------

def build_checklist(project_type: str, auth_type: str) -> str:
    now = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")

    lines = [
        f"# Security Checklist — {project_type.capitalize()} / {auth_type.upper()}",
        "",
        f"> Generated by `generate_security_checklist.py` on {now}  ",
        f"> Project type: **{project_type}** | Auth mechanism: **{auth_type}**",
        "",
        "Use this checklist as a pre-launch security review, a periodic audit baseline, or an onboarding "
        "guide for new team members. Mark items with `[x]` when validated. Flag blockers with `[!]`.",
        "",
        "---",
        "",
        "## 1. Authentication",
        "",
        f"*Rules specific to **{auth_type.upper()}** authentication.*",
        "",
    ]

    # Auth section
    for item in AUTH_CHECKS.get(auth_type, []):
        lines.append(item)

    # Authorization section
    lines += [
        "",
        "---",
        "",
        "## 2. Authorization",
        "",
    ]
    for item in AUTHORIZATION_CHECKS:
        lines.append(item)

    # Data protection section
    lines += [
        "",
        "---",
        "",
        "## 3. Data Protection",
        "",
    ]
    for item in DATA_PROTECTION_CHECKS:
        lines.append(item)

    # Input validation section
    lines += [
        "",
        "---",
        "",
        "## 4. Input Validation",
        "",
        f"*Base rules + rules specific to **{project_type}** projects.*",
        "",
    ]
    for item in BASE_INPUT_CHECKS:
        lines.append(item)
    for item in EXTRA_INPUT_CHECKS.get(project_type, []):
        lines.append(item)

    # Infrastructure section
    lines += [
        "",
        "---",
        "",
        "## 5. Infrastructure & Security Headers",
        "",
    ]
    for item in INFRA_CHECKS:
        lines.append(item)

    # Incident response section
    lines += [
        "",
        "---",
        "",
        "## 6. Incident Response",
        "",
    ]
    for item in INCIDENT_RESPONSE_CHECKS:
        lines.append(item)

    # Summary footer
    total = (
        len(AUTH_CHECKS.get(auth_type, []))
        + len(AUTHORIZATION_CHECKS)
        + len(DATA_PROTECTION_CHECKS)
        + len(BASE_INPUT_CHECKS)
        + len(EXTRA_INPUT_CHECKS.get(project_type, []))
        + len(INFRA_CHECKS)
        + len(INCIDENT_RESPONSE_CHECKS)
    )
    lines += [
        "",
        "---",
        "",
        "## Summary",
        "",
        f"| Section | Items |",
        f"|---------|-------|",
        f"| 1. Authentication ({auth_type.upper()}) | {len(AUTH_CHECKS.get(auth_type, []))} |",
        f"| 2. Authorization | {len(AUTHORIZATION_CHECKS)} |",
        f"| 3. Data Protection | {len(DATA_PROTECTION_CHECKS)} |",
        f"| 4. Input Validation ({project_type}) | {len(BASE_INPUT_CHECKS) + len(EXTRA_INPUT_CHECKS.get(project_type, []))} |",
        f"| 5. Infrastructure & Headers | {len(INFRA_CHECKS)} |",
        f"| 6. Incident Response | {len(INCIDENT_RESPONSE_CHECKS)} |",
        f"| **Total** | **{total}** |",
        "",
        "---",
        "",
        "## References",
        "",
        "- [OWASP Top 10 (2021)](https://owasp.org/Top10/)",
        "- [OWASP ASVS](https://owasp.org/www-project-application-security-verification-standard/)",
        "- [NIST SP 800-63 — Digital Identity Guidelines](https://pages.nist.gov/800-63-3/)",
        "- [OAuth 2.1 Draft](https://oauth.net/2.1/)",
        "- [FIDO2 / WebAuthn](https://webauthn.io/)",
        "- [OWASP Cheat Sheet Series](https://cheatsheetseries.owasp.org/)",
    ]

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description=(
            "Generate a personalised Markdown security checklist based on "
            "project type and authentication mechanism."
        )
    )
    parser.add_argument(
        "--type",
        dest="project_type",
        required=True,
        choices=["webapp", "api", "mobile", "microservices"],
        help="Project type: webapp, api, mobile, or microservices",
    )
    parser.add_argument(
        "--auth",
        dest="auth_type",
        required=True,
        choices=["jwt", "oauth2", "session", "apikey"],
        help="Authentication mechanism: jwt, oauth2, session, or apikey",
    )
    parser.add_argument(
        "--output",
        required=True,
        help="Output file path for the generated Markdown checklist (e.g. security-checklist.md)",
    )

    args = parser.parse_args()

    content = build_checklist(project_type=args.project_type, auth_type=args.auth_type)

    try:
        with open(args.output, "w", encoding="utf-8") as fh:
            fh.write(content)
        # Count total items
        total_items = content.count("[ ]")
        print(f"[OK] Security checklist written to: {args.output}")
        print(f"     Type  : {args.project_type}")
        print(f"     Auth  : {args.auth_type}")
        print(f"     Total checklist items: {total_items}")
    except OSError as exc:
        print(f"Error writing output file: {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
