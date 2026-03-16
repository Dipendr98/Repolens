---
name: gh-security
description: GitHub security posture analysis — branch protection, secret exposure risks, Dependabot status, CodeQL, SECURITY.md, vulnerable dependency signals.
---

# GitHub Security Skill

Assess the security posture of a repository from publicly visible signals.

## Data to Collect

- `GET /repos/{owner}/{repo}` → `private`, `has_vulnerability_alerts_enabled`
- `GET /repos/{owner}/{repo}/branches/{default_branch}` → `protected`, branch protection rules
- `GET /repos/{owner}/{repo}/contents/SECURITY.md` → responsible disclosure policy
- `GET /repos/{owner}/{repo}/contents/.github/dependabot.yml` → Dependabot config
- Scan `.github/workflows/` for CodeQL, Snyk, OWASP, trivy, gitleaks
- Check root for: `.env`, `.env.local`, credentials patterns
- `GET /repos/{owner}/{repo}/vulnerability-alerts` → if token available

## Security Checks

### Branch Protection
- Default branch protected? (requires PR, review, status checks)
- Force push disabled?
- Delete protection enabled?

### Secret Exposure Scan
Look for files that commonly contain secrets:
- `.env*` files committed (bad)
- `*.pem`, `*.key`, `*.pfx` in tree (bad)
- `config/secrets.*` (bad)
- `.env.example` present (good — means they use env vars)

### Dependency Security
- Dependabot alerts enabled? (requires token — note if unknown)
- Dependabot auto-updates configured?
- `package.json` `overrides` / `resolutions` present (patching known vulns)

### Security Workflow Checks
In `.github/workflows/`:
- CodeQL analysis action
- Snyk or similar SCA scanning
- Container scanning (trivy, grype)
- Secret scanning (gitleaks, truffleHog)
- SAST workflow

### Responsible Disclosure
- `SECURITY.md` present
- `SECURITY.md` contains email or contact method
- GitHub's built-in "Report a vulnerability" enabled

## Scoring (0–100)

| Signal | Points |
|---|---|
| Default branch is protected | +25 |
| SECURITY.md present | +15 |
| Dependabot configured | +20 |
| CodeQL or SAST in CI | +20 |
| No suspicious committed files | +15 |
| Secret scanning workflow | +5 |

## Output

1. Security score with grade
2. Branch protection status
3. Security checklist (✅/⚠️/❌ per item)
4. Risk flags (sorted by severity: Critical / High / Medium / Low)
5. Hardening recommendations

## Disclaimer

This is a **surface-level security audit** based on public repo metadata. It does not perform dynamic analysis or deep dependency vulnerability scanning. Recommend using Snyk, Dependabot, or GitHub Advanced Security for production security review.
