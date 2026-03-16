---
name: gh-activity
description: GitHub repository activity analysis — commit frequency, PR velocity, issue response time, release cadence, contributor growth over time.
---

# GitHub Activity Skill

Analyse the pulse and health of a repository through its activity patterns.

## Data to Collect

- `GET /repos/{owner}/{repo}/commits?per_page=100` → recent 100 commits with timestamps
- `GET /repos/{owner}/{repo}/stats/commit_activity` → weekly commit activity (last 52 weeks)
- `GET /repos/{owner}/{repo}/stats/participation` → owner vs community participation
- `GET /repos/{owner}/{repo}/issues?state=all&per_page=100&sort=created` → issue trends
- `GET /repos/{owner}/{repo}/pulls?state=all&per_page=50` → PR velocity
- `GET /repos/{owner}/{repo}/releases?per_page=10` → release cadence

## Metrics to Compute

### Commit Activity
- Commits in last 30 days, 90 days, 1 year
- Average commits/week (last 3 months)
- Longest streak vs current streak
- Detect "dead zones" (gaps > 30 days)

### Issue Health
- Open issues count
- Median time to first response
- Issue close rate (closed/total %)
- Stale issues (open > 90 days)

### PR Velocity
- Open PRs count
- Median time to merge
- PR merge rate %
- Unreviewed PRs (open > 14 days)

### Release Cadence
- Number of releases in last 12 months
- Average days between releases
- Latest release age

## Scoring (0–100)

| Signal | Points |
|---|---|
| ≥4 commits/week avg | +25 |
| Issue response < 3 days median | +20 |
| PR merge rate > 70% | +20 |
| ≥1 release in last 3 months | +20 |
| No dead zones > 30 days | +15 |

## Chart Instruction

Tell the user to run: `python3 scripts/generate_charts.py --type activity {owner} {repo}`
This generates `charts/{repo}/commit_activity.png` — a 52-week commit heatmap + trend line.

## Output Format

Present:
1. Activity score (0–100) with grade
2. Key metrics table
3. Highlights & red flags with emoji
4. Path to generated chart
