<div align="center">

<img src="https://readme-typing-svg.demolab.com?font=Fira+Code&size=13&pause=1000&color=38BDF8&center=true&vCenter=true&width=600&lines=Deep-dive+any+GitHub+repo+in+seconds.;5+parallel+AI+agents.+Scores%2C+charts%2C+PDF+reports.;Built+as+a+Claude+Code+skill." alt="Typing SVG" />

# 🔍 RepoLens

**The GitHub repository analyser you always wished existed — right inside Claude Code.**

[![Claude Code](https://img.shields.io/badge/Claude%20Code-Skill-38bdf8?style=flat-square&logo=anthropic&logoColor=white)](https://docs.anthropic.com/en/docs/claude-code)
[![License: MIT](https://img.shields.io/badge/License-MIT-4ade80?style=flat-square)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.8+-818cf8?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![GitHub API](https://img.shields.io/badge/GitHub%20API-v3-f59e0b?style=flat-square&logo=github)](https://docs.github.com/en/rest)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)](https://github.com/Dipendr98/Repolens/pulls)

[⚡ Install](#installation) · [📖 Commands](#commands) · [🏗️ Architecture](#architecture) · [💡 Use Cases](#use-cases)

</div>

---

## What Is RepoLens?

You find a GitHub repo. You want to know: *Is this safe to depend on? Is it actually maintained? Does one person hold everything together? Are there security gaps?*

Opening the repo manually tells you almost nothing. Stars can be bought. Last-commit dates lie. A beautiful README can hide a dead project.

**RepoLens sees through all of that.**

Drop any GitHub URL into [Claude Code](https://docs.anthropic.com/en/docs/claude-code) and 5 parallel AI agents immediately go to work — pulling real data from the GitHub API, computing scores across 5 dimensions, generating publication-quality charts, and assembling a professional PDF report. All in under a minute. All from a single terminal command. No dashboards, no sign-ups, no waiting.

```
> /github analyse https://github.com/supabase/supabase

Launching 5 parallel agents...
✓ Code Quality          — Score: 82/100
✓ Activity & Health     — Score: 91/100
✓ Community             — Score: 78/100
✓ Security              — Score: 65/100
✓ Documentation & DX    — Score: 87/100

Overall Repository Score: 81/100  [Grade: B]

📁 Full report → GITHUB-ANALYSIS-supabase.md
📈 Charts      → charts/supabase/
```

> 💡 **RepoLens is a [Claude Code skill](https://docs.anthropic.com/en/docs/claude-code)** — a structured set of AI instructions that live in your terminal and turn Claude into a full-featured repository intelligence tool.

---

## Installation

### ⚡ One Command

```bash
curl -fsSL https://raw.githubusercontent.com/Dipendr98/Repolens/main/install.sh | bash
```

### Manual

```bash
git clone https://github.com/Dipendr98/Repolens.git
cd Repolens
chmod +x install.sh && ./install.sh
```

### PDF Reports (Optional but Recommended)

```bash
pip install reportlab matplotlib numpy
```

That's it. Open Claude Code and start analysing.

---

## Commands

| Command | What It Does |
|---|---|
| `/github analyse <url>` | 🔬 Full deep analysis — 5 agents, all charts, scored report |
| `/github overview <url>` | 📦 Quick metadata: stars, forks, language, license, topics |
| `/github activity <url>` | 📈 Commit heatmap, PR velocity, issue response time |
| `/github contributors <url>` | 👥 Bus factor, top contributors, community health |
| `/github code <url>` | 🧪 Code quality, CI/CD config, test coverage signals |
| `/github security <url>` | 🔒 Branch protection, Dependabot, CodeQL, secrets scan |
| `/github compare <url1> <url2>` | ⚖️ Side-by-side repo comparison |
| `/github report <url>` | 📄 Full structured Markdown report |
| `/github report-pdf <url>` | 📑 Professional multi-page PDF with embedded charts |

---

## How It Works

RepoLens is a **Claude Code skill** — a set of instruction files that tell Claude exactly how to analyse, score, and visualise GitHub repositories. When you run a command, Claude orchestrates the whole pipeline:

```
You type /github analyse <url>
         │
         ▼
┌─────────────────────────────┐
│   SKILL.md (Orchestrator)   │
│   Parses URL, routes task   │
└────────────┬────────────────┘
             │  spawns
    ┌────────▼─────────────────────────────────────┐
    │            5 Parallel Agents                  │
    │  ┌──────────┐  ┌──────────┐  ┌────────────┐  │
    │  │   Code   │  │ Activity │  │ Community  │  │
    │  │ Quality  │  │  Health  │  │ & Bus Fac. │  │
    │  └──────────┘  └──────────┘  └────────────┘  │
    │       ┌────────────┐  ┌──────────────┐        │
    │       │  Security  │  │  Docs & DX   │        │
    │       └────────────┘  └──────────────┘        │
    └──────────────────┬───────────────────────────┘
                       │
    ┌──────────────────▼───────────────────────────┐
    │           Python Scripts                       │
    │  fetch_repo.py  → GitHub API → local cache     │
    │  generate_charts.py → 5 chart types            │
    │  generate_pdf_report.py → multi-page PDF       │
    └──────────────────┬───────────────────────────┘
                       │
               Scored report + charts + PDF
```

---

## Scoring Methodology

Every repository is graded across 5 dimensions:

| Dimension | Weight | What It Measures |
|---|---|---|
| 🧪 Code Quality | 25% | Tests, CI/CD, types, structure, containerisation |
| 📈 Activity & Health | 20% | Commit cadence, PR velocity, issue response time |
| 👥 Community | 20% | Bus factor, contributor diversity, governance |
| 🔒 Security | 20% | Branch protection, Dependabot, CodeQL, secrets |
| 📄 Docs & DX | 15% | README quality, CHANGELOG, API docs, examples |

**Grades:** `A` (90+) · `B` (75–89) · `C` (60–74) · `D` (40–59) · `F` (<40)

---

## Charts Generated

Every full analysis produces 5 ready-to-share charts:

| Chart | What it shows |
|---|---|
| 🗓️ **52-Week Commit Heatmap** | GitHub-style activity grid — see exactly when development was active |
| 📈 **Weekly Commit Trend** | 26-week line chart with 4-week moving average |
| 👥 **Contributor Breakdown** | Pie (share) + bar chart (commits) for top contributors |
| 🔤 **Language Distribution** | Donut chart of the codebase language split |
| 🐛 **Issues & PRs Overview** | Open vs closed — at a glance |

---

## Use Cases

**🧑‍💻 For Developers**
Evaluating a new library before `npm install`? Run `/github analyse` first. Check the bus factor, security posture, and maintenance health before your project depends on something that might break tomorrow.

**🏢 For Technical Due Diligence**
Assessing an open-source project for enterprise adoption? Generate `/github report-pdf` and hand it to your engineering lead. It's a multi-page professional document — not a raw API dump.

**⚖️ For Comparing Alternatives**
Can't decide between two state management libraries? `/github compare <url1> <url2>` gives you a head-to-head breakdown across every dimension so you pick with confidence, not guesswork.

**🛠️ For Maintainers**
Audit your own repo before open-sourcing it. RepoLens will surface your bus factor risk, missing security configs, documentation gaps, and hand you a prioritised list of what to fix first.

**💼 For Investors & Founders**
Doing technical due diligence on a startup's open-source stack? RepoLens generates the kind of structured, scored report that belongs in a data room.

---

## Architecture

```
Repolens/
├── SKILL.md                          # Main orchestrator — routes all /github commands
│
├── skills/
│   ├── gh-overview/SKILL.md          # Metadata + quick stats
│   ├── gh-activity/SKILL.md          # Commit + issue + PR analysis
│   ├── gh-contributors/SKILL.md      # Bus factor + contributor map
│   ├── gh-code-quality/SKILL.md      # Code structure + CI/CD signals
│   ├── gh-security/SKILL.md          # Security posture audit
│   ├── gh-compare/SKILL.md           # Side-by-side comparison
│   ├── gh-report/SKILL.md            # Markdown report generator
│   └── gh-report-pdf/SKILL.md        # PDF report generator
│
├── agents/
│   ├── gh-code-agent.md              # Code quality subagent
│   ├── gh-activity-agent.md          # Activity & health subagent
│   ├── gh-community-agent.md         # Community & contributors subagent
│   ├── gh-security-agent.md          # Security posture subagent
│   └── gh-docs-agent.md              # Documentation & DX subagent
│
├── scripts/
│   ├── fetch_repo.py                 # GitHub API fetcher with local cache
│   ├── generate_charts.py            # 5 chart types via matplotlib
│   └── generate_pdf_report.py        # Multi-page PDF via reportlab
│
├── templates/
│   └── report-template.md            # Structured Markdown report template
│
├── install.sh                        # One-command installer
├── uninstall.sh                      # Clean uninstaller
└── requirements.txt                  # Python dependencies
```

---

## GitHub Token (Recommended)

RepoLens works without a token, but the GitHub API rate-limits unauthenticated requests to **60/hour**.

With a personal access token you get **5,000 requests/hour** plus access to additional endpoints (branch protection, vulnerability alerts, community profiles).

```bash
export GITHUB_TOKEN=ghp_your_personal_access_token
```

Create one at: **GitHub → Settings → Developer Settings → Personal Access Tokens → Tokens (classic)** — only `public_repo` scope needed for public repos.

---

## Requirements

- [Claude Code](https://docs.anthropic.com/en/docs/claude-code) installed
- Python 3.8+
- `pip install requests matplotlib numpy` (auto-installed by `install.sh`)
- `pip install reportlab` (optional, for PDF reports)

---

## Uninstall

```bash
./uninstall.sh
```

---

## Contributing

Pull requests are welcome. If you want to add a new analysis dimension, a new chart type, or support for GitLab / Bitbucket — open an issue and let's talk.

---

## License

MIT — use it, fork it, build on it.

If RepoLens saved you time, a ⭐ on the repo goes a long way.

---

<div align="center">

**Built with 🔍 by [Dipendr98](https://github.com/Dipendr98)**

*RepoLens is a Claude Code skill — not an official Anthropic product.*

</div>
