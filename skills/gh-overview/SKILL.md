---
name: gh-overview
description: GitHub repository overview — metadata, stars, forks, language breakdown, topics, license, open issues summary.
---

# GitHub Overview Skill

Fetch and present a rich overview of any GitHub repository.

## Data to Collect

Call the GitHub API:
- `GET /repos/{owner}/{repo}` → stars, forks, watchers, open_issues_count, language, license, created_at, pushed_at, size, topics, description, homepage, archived, disabled
- `GET /repos/{owner}/{repo}/languages` → language breakdown (bytes)
- `GET /repos/{owner}/{repo}/releases?per_page=1` → latest release tag + date
- `GET /repos/{owner}/{repo}/contents/README.md` → check if exists
- `GET /repos/{owner}/{repo}/contents/.github` → check for workflows, templates

## Output Format

Present as a structured card:

```
┌─────────────────────────────────────────────────┐
│  📦  owner/repo                                  │
│  ⭐ 1,234 stars  🍴 89 forks  👁️ 45 watchers     │
│  🔤 Primary language: TypeScript                 │
│  📅 Created: Jan 2023 | Last push: 2 days ago   │
│  🏷️  Latest release: v2.1.0 (3 weeks ago)        │
│  📄 License: MIT                                 │
│  🏷️  Topics: react, typescript, saas, tailwind   │
└─────────────────────────────────────────────────┘
```

Then a language breakdown table:
| Language | % |
|---|---|
| TypeScript | 68% |
| CSS | 18% |
| HTML | 9% |
| Shell | 5% |

## Signals to Flag

- ⚠️ If `archived: true` → mark as ARCHIVED
- ⚠️ If last push > 6 months → "low recent activity"
- ⚠️ If no license → "no license detected"
- ✅ If has homepage → "live demo available"
- ✅ If has .github/workflows → "CI/CD configured"
