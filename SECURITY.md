# Security Policy

## Supported Versions

We provide security updates for the **latest minor version** of each product in the Trindade SDD ecosystem. Older versions receive critical patches only when feasible.

| Product | Current Version | Supported |
|---|---|---|
| PreForja | 0.3.x | :white_check_mark: |
| Forja | 1.3.x | :white_check_mark: |
| Visa | 1.4.x | :white_check_mark: |
| paridade-guard | 0.3.x | :white_check_mark: |
| Genese | 1.0.x | :white_check_mark: |
| Regente | 1.0.x | :white_check_mark: |
| Reversa | maintained by [@sandeco](https://github.com/sandeco) | see their policy |

## Reporting a Vulnerability

**Do not open a public GitHub issue for security vulnerabilities.**

Instead, use one of these private channels:

1. **GitHub Security Advisories** (preferred): use the "Report a vulnerability" button under the Security tab of the affected repo
2. **Email:** adgmed2018@gmail.com with subject `[SECURITY] <product> <brief description>`

### What to Include

- Product and version affected
- Type of vulnerability (RCE, path traversal, prototype pollution, etc.)
- Steps to reproduce
- Potential impact
- Your contact for follow-up

### Our Commitment

| Step | SLA |
|---|---|
| Acknowledgment | Within 48 hours |
| Initial assessment | Within 7 days |
| Fix for critical (RCE, exfiltration) | Within 14 days |
| Fix for high (DoS, auth bypass) | Within 30 days |
| Fix for medium/low | Next regular release |
| Public disclosure | Coordinated with reporter (typically 90 days after fix) |

We follow [responsible disclosure](https://en.wikipedia.org/wiki/Coordinated_vulnerability_disclosure) practices.

### Recognition

Security researchers who report valid vulnerabilities will be credited in the release notes (unless they request anonymity). We don't currently have a paid bug bounty, but **legitimate finds get public acknowledgment and our gratitude**.

## Security Best Practices for Users

If you use Trindade SDD tools in production:

- **Pin versions** in your `package.json` / `pyproject.toml` (avoid `^` for major dependencies)
- **Enable Renovate or Dependabot** to track CVE alerts
- **Run `npm audit` / `pip-audit`** in your CI
- **Don't commit** `state.json` if it contains sensitive data
- **Review manifest hashes** after `update` if running in regulated environments

## Threat Model Assumptions

Trindade SDD tools are **developer tools**, not production runtime components. Threats we explicitly consider:

- :white_check_mark: Malicious npm/PyPI tarballs (mitigated via OIDC provenance)
- :white_check_mark: Path traversal in `--output` flags (mitigated via path validation)
- :white_check_mark: Prototype pollution from user input (mitigated via JSON Schema validation)

Threats **NOT** in our model:

- :x: Malicious LLM generating malicious code (your responsibility -- review what agents produce)
- :x: Compromised IDE or terminal (out of scope)
- :x: Local filesystem with malicious files (we trust the project root)

## Hall of Fame

(Empty for now. Be the first?)

---

Last updated: 2026-05-08