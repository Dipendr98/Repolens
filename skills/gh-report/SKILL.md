---
name: gh-report
description: Generate a full, professional Markdown report for a GitHub repository combining all analysis dimensions with charts, scores, and actionable recommendations.
---

# GitHub Report Skill (Markdown)

Generate a comprehensive, client-ready Markdown report.

## Execution Steps

1. Run all 5 sub-analyses (code quality, activity, contributors, security, docs)
2. Generate all charts via `python3 scripts/generate_charts.py {owner} {repo}`
3. Compile into a single Markdown file using `templates/report-template.md`
4. Save as `GITHUB-REPORT-{repo}.md`

## Report Sections

```markdown
# 📊 GitHub Repository Analysis: owner/repo
> Generated: {date} | Analyst: GitHub Analyser v1.0

## Executive Summary
[2-3 sentence TL;DR with overall score and grade]

## Repository Overview
[Overview card from gh-overview skill]

## Scores Dashboard
[Table of all 5 dimension scores + overall]

## 1. Code Quality Analysis [XX/100]
[Full code quality output + chart reference]

## 2. Activity & Health [XX/100]
[Activity output + commit heatmap chart]

## 3. Community & Contributors [XX/100]
[Contributors output + pie chart]

## 4. Security Posture [XX/100]
[Security output + checklist]

## 5. Documentation & DX [XX/100]
[Docs output + checklist]

## Top 10 Actionable Recommendations
[Prioritised list — Critical → High → Medium → Low]

## Tech Stack Summary
[Detected languages, frameworks, tools]

## Conclusion
[Final verdict, best use cases, adoption recommendation]
```

## Chart References

Embed charts as relative image links:
```markdown
![Commit Activity](charts/{repo}/commit_activity.png)
![Contributors](charts/{repo}/contributor_pie.png)
![Score Radar](charts/{repo}/score_radar.png)
```

## Tone

Professional and objective. Suitable to send to:
- A CTO evaluating a library for adoption
- An investor doing technical due diligence
- An open source maintainer wanting improvement feedback
