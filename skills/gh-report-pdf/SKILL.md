---
name: gh-report-pdf
description: Generate a professional PDF report for a GitHub repository with charts, scores radar, and formatted sections. Requires reportlab and matplotlib.
---

# GitHub Report PDF Skill

Generate a polished PDF report with embedded charts.

## Prerequisites

```bash
pip install reportlab matplotlib numpy requests
```

## Execution

1. Run full analysis (same as `/github report`)
2. Generate all charts: `python3 scripts/generate_charts.py {owner} {repo}`
3. Generate PDF: `python3 scripts/generate_pdf_report.py {owner} {repo}`
4. Output: `GITHUB-REPORT-{repo}.pdf`

## PDF Structure

**Page 1 — Cover**
- Repository name + description
- Overall score (large, styled)
- Generated date
- Repository avatar/preview

**Page 2 — Executive Summary + Scores**
- Score radar chart (all 5 dimensions)
- Executive summary paragraph
- Quick stats table

**Page 3 — Activity Analysis**
- 52-week commit heatmap
- Weekly trend line
- Key metrics

**Page 4 — Contributors**
- Contributor pie chart
- Top 10 table
- Bus factor risk indicator

**Page 5 — Code Quality & Security**
- Tech stack summary
- CI/CD pipeline diagram (text-based)
- Security checklist

**Page 6 — Recommendations**
- Prioritised action items (Critical/High/Medium/Low)
- Conclusion paragraph

## Style

- Font: Helvetica
- Primary colour: #1a1a2e (dark navy)
- Accent: #4CAF50 (green for good), #f44336 (red for risks)
- Score badges: colour-coded by grade
- Professional, clean layout

## Script Location

`scripts/generate_pdf_report.py` — handles all PDF generation using reportlab.
