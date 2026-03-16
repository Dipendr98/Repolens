---
name: github-analyser
description: >
  Comprehensive GitHub repository analysis suite. Use this skill whenever the user
  wants to analyse, audit, inspect, review, or generate a report for any GitHub
  repository. Triggers on any mention of: "analyse this repo", "GitHub report",
  "repo health", "contributor stats", "code quality", "commit activity", "compare
  repos", "repo insights", "/github", or when a github.com URL is provided and
  analysis is requested. Generates scored reports, charts, and PDF deliverables.
  Always use this skill for any GitHub repository analysis task — even if the user
  just pastes a GitHub URL and says "check this out" or "what do you think of this".
---

# GitHub Analyser — Main Orchestrator

You are the GitHub Analyser orchestrator. Route `/github` commands to the correct sub-skill based on the table below. Always read the relevant sub-skill's SKILL.md before proceeding.

## Command Routing

| Command | Sub-skill to read | What it does |
|---|---|---|
| `/github analyse <url>` | `skills/gh-overview/SKILL.md` + run 5 agents | Full deep analysis with scoring |
| `/github overview <url>` | `skills/gh-overview/SKILL.md` | Quick overview & metadata |
| `/github activity <url>` | `skills/gh-activity/SKILL.md` | Commit trends, release cadence, pulse |
| `/github contributors <url>` | `skills/gh-contributors/SKILL.md` | Contributor map, bus factor, diversity |
| `/github code <url>` | `skills/gh-code-quality/SKILL.md` | Code quality, complexity, tech debt signals |
| `/github security <url>` | `skills/gh-security/SKILL.md` | Security posture, dependency risks, secrets scan |
| `/github compare <url1> <url2>` | `skills/gh-compare/SKILL.md` | Side-by-side repo comparison |
| `/github report <url>` | `skills/gh-report/SKILL.md` | Full Markdown report |
| `/github report-pdf <url>` | `skills/gh-report-pdf/SKILL.md` | Professional PDF report with charts |

## Fallback: No command prefix

If the user pastes a GitHub URL without a `/github` prefix but asks for analysis, default to `/github analyse`.

## Execution Pattern for `/github analyse`

1. Read `skills/gh-overview/SKILL.md`
2. Run the Python fetch script: `python3 scripts/fetch_repo.py <owner> <repo>`
3. Launch 5 parallel analysis agents (read `agents/` files):
   - `agents/gh-code-agent.md` → Code quality score
   - `agents/gh-activity-agent.md` → Activity & health score
   - `agents/gh-community-agent.md` → Community & contributor score
   - `agents/gh-security-agent.md` → Security posture score
   - `agents/gh-docs-agent.md` → Documentation & DX score
4. Generate charts: `python3 scripts/generate_charts.py <owner> <repo>`
5. Compile results into a scored summary (see scoring below)
6. Save full report as `GITHUB-ANALYSIS-<repo>.md`

## Overall Scoring

| Dimension | Weight | What it measures |
|---|---|---|
| Code Quality | 25% | Structure, complexity, test coverage signals, tech debt |
| Activity & Health | 20% | Commit cadence, issue response time, PR merge rate |
| Community | 20% | Contributors, bus factor, governance, COC |
| Security | 20% | Dependency vulnerabilities, secret exposure, branch protection |
| Documentation & DX | 15% | README quality, API docs, contributing guide, CI/CD |

**Overall Score** = weighted average (0–100). Grade: A (90+), B (75–89), C (60–74), D (40–59), F (<40)

## Output Format

Always present:
```
📊 GitHub Analysis: <owner>/<repo>
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✓ Code Quality          — Score: XX/100
✓ Activity & Health     — Score: XX/100
✓ Community             — Score: XX/100
✓ Security              — Score: XX/100
✓ Documentation & DX    — Score: XX/100
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Overall Repository Score: XX/100  [Grade: X]

📁 Full report saved to GITHUB-ANALYSIS-<repo>.md
📈 Charts saved to charts/<repo>/
```

## Parsing GitHub URLs

Supported formats:
- `https://github.com/owner/repo`
- `https://github.com/owner/repo/tree/branch`
- `github.com/owner/repo`
- `owner/repo` (short form)

Extract `owner` and `repo` from any of these.

## GitHub API Base URL

`https://api.github.com/repos/{owner}/{repo}`

If the user provides a `GITHUB_TOKEN` env variable, include it as `Authorization: Bearer <token>` header to increase rate limits and access private repos.

## Error Handling

- If repo is private and no token: inform the user, suggest setting `GITHUB_TOKEN`
- If rate limited (403): suggest waiting or providing a token
- If repo not found (404): verify the URL with the user
