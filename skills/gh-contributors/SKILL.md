---
name: gh-contributors
description: GitHub contributor analysis — bus factor, top contributors, contribution distribution, community health, new vs returning contributor ratio.
---

# GitHub Contributors Skill

Deep-dive into who builds and maintains the repository.

## Data to Collect

- `GET /repos/{owner}/{repo}/contributors?per_page=100` → all contributors, commit counts
- `GET /repos/{owner}/{repo}/stats/contributors` → weekly additions/deletions per contributor
- `GET /repos/{owner}/{repo}/community/profile` → community health score, COC, CONTRIBUTING, templates
- `GET /repos/{owner}/{repo}/contents/CONTRIBUTING.md` → exists check
- `GET /repos/{owner}/{repo}/contents/CODE_OF_CONDUCT.md` → exists check

## Metrics to Compute

### Bus Factor
Percentage of commits from top 1 and top 3 contributors.
- Top 1 > 70% of commits → Bus Factor = 1 (🚨 critical risk)
- Top 3 > 80% of commits → Bus Factor ≈ 2–3 (⚠️ moderate risk)
- Distributed → Bus Factor = healthy (✅)

### Contribution Distribution
Create a Gini-like inequality score:
- 0 = perfectly equal
- 1 = one person does everything
Show top 10 contributors as a ranked table with % share.

### Community Health Checklist
- [ ] CONTRIBUTING.md present
- [ ] CODE_OF_CONDUCT.md present
- [ ] Issue templates present
- [ ] PR templates present
- [ ] GitHub Discussions enabled
- [ ] Sponsor button / funding

### Activity Recency
Classify contributors as:
- **Active** (commit in last 30 days)
- **Recent** (commit in last 90 days)
- **Dormant** (last commit > 90 days)

## Scoring (0–100)

| Signal | Points |
|---|---|
| Bus factor ≥ 3 | +25 |
| CONTRIBUTING.md present | +15 |
| CODE_OF_CONDUCT.md present | +10 |
| ≥ 3 active contributors | +20 |
| Issue + PR templates present | +15 |
| Gini score < 0.6 | +15 |

## Chart Instruction

Run: `python3 scripts/generate_charts.py --type contributors {owner} {repo}`
Generates:
- `charts/{repo}/contributor_pie.png` — top 10 contribution share pie
- `charts/{repo}/contributor_bar.png` — commits per contributor bar chart

## Output

1. Bus factor assessment with risk level
2. Top 10 contributors table
3. Community health checklist
4. Contributor score with grade
5. Recommendations (e.g., "Recruit more maintainers", "Add CONTRIBUTING.md")
