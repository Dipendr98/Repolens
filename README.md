# 📊 GitHub Analyser — Skill Suite for Claude Code

A comprehensive GitHub repository analysis system for [Claude Code](https://docs.anthropic.com/en/docs/claude-code).
Analyse any public repo's health, code quality, security posture, contributor dynamics, and activity — then generate scored reports and professional PDF deliverables.

---

## What You Get

Type a command and get instant, multi-dimensional analysis:

```
> /github analyse https://github.com/supabase/supabase

Launching 5 parallel agents...
✓ Code Quality          — Score: 82/100
✓ Activity & Health     — Score: 91/100
✓ Community             — Score: 78/100
✓ Security              — Score: 65/100
✓ Documentation & DX    — Score: 87/100

Overall Repository Score: 81/100  [Grade: B]

📁 Full report saved to GITHUB-ANALYSIS-supabase.md
📈 Charts saved to charts/supabase/
```

---

## Installation

### One-Command Install
```bash
curl -fsSL https://raw.githubusercontent.com/YOUR_USERNAME/github-analyser/main/install.sh | bash
```

### Manual Install
```bash
git clone https://github.com/YOUR_USERNAME/github-analyser.git
cd github-analyser
chmod +x install.sh && ./install.sh
```

### Optional: PDF Report Support
```bash
pip install reportlab matplotlib numpy
```

---

## Commands

| Command | What It Does |
|---|---|
| `/github analyse <url>` | Full analysis with 5 parallel agents + all charts |
| `/github overview <url>` | Quick metadata overview |
| `/github activity <url>` | Commit trends, issue velocity, PR cadence |
| `/github contributors <url>` | Bus factor, contributor map, community health |
| `/github code <url>` | Code quality, CI/CD, test coverage signals |
| `/github security <url>` | Security posture, branch protection, dependency risks |
| `/github compare <url1> <url2>` | Side-by-side repo comparison |
| `/github report <url>` | Full Markdown report |
| `/github report-pdf <url>` | Professional PDF with embedded charts |

---

## Scoring Methodology

| Dimension | Weight | What It Measures |
|---|---|---|
| Code Quality | 25% | Structure, tests, CI/CD, types, containerization |
| Activity & Health | 20% | Commit cadence, issue response, PR velocity |
| Community | 20% | Bus factor, contributors, governance, COC |
| Security | 20% | Branch protection, Dependabot, CodeQL, secrets |
| Documentation & DX | 15% | README quality, CHANGELOG, API docs, examples |

**Grade:** A (90+) · B (75–89) · C (60–74) · D (40–59) · F (<40)

---

## Architecture

```
github-analyser/
├── SKILL.md                          # Main orchestrator (routes /github commands)
│
├── skills/
│   ├── gh-overview/SKILL.md          # Quick repo overview
│   ├── gh-activity/SKILL.md          # Activity & pulse analysis
│   ├── gh-contributors/SKILL.md      # Contributor & community analysis
│   ├── gh-code-quality/SKILL.md      # Code quality signals
│   ├── gh-security/SKILL.md          # Security posture
│   ├── gh-compare/SKILL.md           # Side-by-side comparison
│   ├── gh-report/SKILL.md            # Markdown report
│   └── gh-report-pdf/SKILL.md        # PDF report
│
├── agents/
│   ├── gh-code-agent.md              # Code quality subagent
│   ├── gh-activity-agent.md          # Activity subagent
│   ├── gh-community-agent.md         # Community subagent
│   ├── gh-security-agent.md          # Security subagent
│   └── gh-docs-agent.md              # Docs & DX subagent
│
├── scripts/
│   ├── fetch_repo.py                 # GitHub API data fetcher + cache
│   ├── generate_charts.py            # All chart generation (matplotlib)
│   └── generate_pdf_report.py        # Professional PDF (reportlab)
│
├── templates/
│   └── report-template.md            # Markdown report template
│
├── install.sh
├── uninstall.sh
└── requirements.txt
```

---

## GitHub Token (Recommended)

Without a token: 60 requests/hour (usually sufficient for one analysis).
With a token: 5,000 requests/hour + access to more API endpoints.

```bash
export GITHUB_TOKEN=ghp_your_token_here
```

---

## Use Cases

**For Developers:**
- Evaluate a library before adding it as a dependency
- Audit your own repo before open-sourcing
- Compare alternatives side-by-side

**For Technical Due Diligence:**
- Assess an open source project for enterprise adoption
- Evaluate a startup's codebase health
- Generate a client-ready PDF report

**For Maintainers:**
- Identify gaps in your security posture
- Track contributor health and bus factor
- Get prioritised improvement recommendations

---

## Uninstall

```bash
./uninstall.sh
```

---

## License

MIT
