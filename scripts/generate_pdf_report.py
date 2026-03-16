#!/usr/bin/env python3
"""
generate_pdf_report.py — Generate a professional PDF report for a GitHub repository.
Usage: python3 scripts/generate_pdf_report.py <owner> <repo> [--scores JSON]
Requires: pip install reportlab matplotlib numpy requests
"""

import sys
import os
import json
import argparse
from pathlib import Path
from datetime import datetime, timezone

try:
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import cm, mm
    from reportlab.lib.colors import HexColor, white, black
    from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table,
                                     TableStyle, Image, PageBreak, HRFlowable,
                                     KeepTogether)
    from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
    from reportlab.graphics.shapes import Drawing, Rect, String, Line
    from reportlab.graphics import renderPDF
except ImportError:
    print("Installing reportlab...")
    os.system("pip install reportlab --break-system-packages -q")
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import cm, mm
    from reportlab.lib.colors import HexColor, white, black
    from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table,
                                     TableStyle, Image, PageBreak, HRFlowable,
                                     KeepTogether)
    from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
    from reportlab.graphics.shapes import Drawing, Rect, String
    from reportlab.graphics import renderPDF

# Colours
C_NAVY   = HexColor("#1a1a2e")
C_BLUE   = HexColor("#16213e")
C_ACCENT = HexColor("#0f3460")
C_GREEN  = HexColor("#4CAF50")
C_RED    = HexColor("#f44336")
C_ORANGE = HexColor("#FF9800")
C_YELLOW = HexColor("#FFC107")
C_GREY   = HexColor("#9e9e9e")
C_LIGHT  = HexColor("#e0e0e0")
C_WHITE  = white
C_TEXT   = HexColor("#212121")
C_SUBTEXT = HexColor("#555555")

PAGE_W, PAGE_H = A4


def grade_colour(score):
    if score >= 90: return C_GREEN
    if score >= 75: return HexColor("#8BC34A")
    if score >= 60: return C_YELLOW
    if score >= 40: return C_ORANGE
    return C_RED


def score_to_grade(score):
    if score >= 90: return "A"
    if score >= 75: return "B"
    if score >= 60: return "C"
    if score >= 40: return "D"
    return "F"


def load_data(owner, repo, data_dir="."):
    cache_file = Path(data_dir) / "cache" / f"{owner}_{repo}_data.json"
    if not cache_file.exists():
        print(f"❌ No cached data at {cache_file}")
        print(f"   Run: python3 scripts/fetch_repo.py {owner} {repo}")
        sys.exit(1)
    with open(cache_file) as f:
        return json.load(f)


def make_styles():
    styles = getSampleStyleSheet()
    custom = {
        "Title": ParagraphStyle("Title", fontName="Helvetica-Bold", fontSize=28, textColor=C_NAVY,
                                 spaceAfter=6, leading=34, alignment=TA_CENTER),
        "Subtitle": ParagraphStyle("Subtitle", fontName="Helvetica", fontSize=13, textColor=C_SUBTEXT,
                                    spaceAfter=12, leading=18, alignment=TA_CENTER),
        "H1": ParagraphStyle("H1", fontName="Helvetica-Bold", fontSize=18, textColor=C_NAVY,
                              spaceBefore=16, spaceAfter=6, leading=22),
        "H2": ParagraphStyle("H2", fontName="Helvetica-Bold", fontSize=13, textColor=C_ACCENT,
                              spaceBefore=10, spaceAfter=4, leading=16),
        "Body": ParagraphStyle("Body", fontName="Helvetica", fontSize=10, textColor=C_TEXT,
                                spaceAfter=4, leading=14),
        "Small": ParagraphStyle("Small", fontName="Helvetica", fontSize=8, textColor=C_SUBTEXT,
                                 spaceAfter=2, leading=11),
        "Label": ParagraphStyle("Label", fontName="Helvetica-Bold", fontSize=9, textColor=C_SUBTEXT,
                                 spaceAfter=2, leading=12),
        "Check": ParagraphStyle("Check", fontName="Helvetica", fontSize=9, textColor=C_TEXT,
                                 leftIndent=10, spaceAfter=2, leading=13),
        "Rec": ParagraphStyle("Rec", fontName="Helvetica", fontSize=9, textColor=C_TEXT,
                               leftIndent=12, spaceAfter=3, leading=13),
        "Code": ParagraphStyle("Code", fontName="Courier", fontSize=8, textColor=HexColor("#1a237e"),
                                backColor=HexColor("#f5f5f5"), spaceAfter=4, leading=12, leftIndent=8),
    }
    return custom


def score_badge_table(scores):
    """Returns a ReportLab Table showing dimension scores."""
    dims = [
        ("Code Quality", scores.get("code_quality", 0), "25%"),
        ("Activity & Health", scores.get("activity", 0), "20%"),
        ("Community", scores.get("community", 0), "20%"),
        ("Security", scores.get("security", 0), "20%"),
        ("Docs & DX", scores.get("docs", 0), "15%"),
    ]
    overall = round(
        dims[0][1] * 0.25 + dims[1][1] * 0.20 + dims[2][1] * 0.20 +
        dims[3][1] * 0.20 + dims[4][1] * 0.15
    )
    grade = score_to_grade(overall)

    table_data = [["Dimension", "Score", "Grade", "Weight"]]
    for name, score, weight in dims:
        g = score_to_grade(score)
        table_data.append([name, f"{score}/100", g, weight])
    table_data.append(["OVERALL", f"{overall}/100", grade, "—"])

    col_widths = [8*cm, 3*cm, 2.5*cm, 2.5*cm]
    t = Table(table_data, colWidths=col_widths)

    style = TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), C_NAVY),
        ("TEXTCOLOR", (0, 0), (-1, 0), C_WHITE),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, 0), 10),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("ALIGN", (0, 0), (0, -1), "LEFT"),
        ("FONTNAME", (0, -1), (-1, -1), "Helvetica-Bold"),
        ("BACKGROUND", (0, -1), (-1, -1), C_ACCENT),
        ("TEXTCOLOR", (0, -1), (-1, -1), C_WHITE),
        ("ROWBACKGROUNDS", (0, 1), (-1, -2), [HexColor("#f5f5f5"), C_WHITE]),
        ("GRID", (0, 0), (-1, -1), 0.3, C_GREY),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
    ])
    # Colour grade cells
    for row_i, (_, score, _2) in enumerate(dims, 1):
        g = score_to_grade(score)
        gc = grade_colour(score)
        style.add("TEXTCOLOR", (2, row_i), (2, row_i), gc)
        style.add("FONTNAME", (2, row_i), (2, row_i), "Helvetica-Bold")

    t.setStyle(style)
    return t, overall, grade


def stats_table(summary):
    data = [
        ["⭐ Stars", f"{summary.get('stars', 0):,}", "🍴 Forks", f"{summary.get('forks', 0):,}"],
        ["👥 Contributors", str(summary.get("total_contributors", 0)),
         "🐛 Open Issues", str(summary.get("open_issues", 0))],
        ["📦 Language", summary.get("primary_language", "—"),
         "📄 License", summary.get("license", "—")],
        ["🏷️  Latest Release", summary.get("latest_release", "—"),
         "📅 Last Pushed", summary.get("pushed_at", "—")[:10]],
        ["📈 Commits/30d", str(summary.get("commits_last_30d", 0)),
         "📊 Avg/week", str(summary.get("avg_commits_per_week", 0))],
    ]
    col_widths = [4.5*cm, 4*cm, 4.5*cm, 4*cm]
    t = Table(data, colWidths=col_widths)
    t.setStyle(TableStyle([
        ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
        ("FONTNAME", (2, 0), (2, -1), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("TEXTCOLOR", (0, 0), (0, -1), C_SUBTEXT),
        ("TEXTCOLOR", (2, 0), (2, -1), C_SUBTEXT),
        ("ROWBACKGROUNDS", (0, 0), (-1, -1), [HexColor("#f9f9f9"), C_WHITE]),
        ("GRID", (0, 0), (-1, -1), 0.3, C_LIGHT),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
    ]))
    return t


def checklist_items(checks_dict, labels_map):
    items = []
    for key, label in labels_map.items():
        val = checks_dict.get(key, False)
        icon = "✅" if val else "❌"
        items.append(f"{icon}  {label}")
    return items


def build_report(owner, repo, data, scores, out_path):
    summary = data.get("summary", {})
    styles = make_styles()
    story = []

    # ─── COVER PAGE ──────────────────────────────────────────────────────────
    story.append(Spacer(1, 2*cm))
    story.append(Paragraph("📊 GitHub Repository Analysis", styles["Title"]))
    story.append(Paragraph(f"{owner} / {repo}", styles["Subtitle"]))
    story.append(Spacer(1, 0.3*cm))

    if summary.get("description"):
        story.append(Paragraph(f'<i>"{summary["description"]}"</i>', styles["Body"]))

    story.append(Spacer(1, 0.5*cm))
    story.append(HRFlowable(width="100%", thickness=1, color=C_LIGHT))
    story.append(Spacer(1, 0.3*cm))

    # Quick stats
    story.append(stats_table(summary))
    story.append(Spacer(1, 0.8*cm))

    # Score table
    story.append(Paragraph("Overall Scores", styles["H1"]))
    score_tbl, overall, grade = score_badge_table(scores)
    story.append(score_tbl)
    story.append(Spacer(1, 0.5*cm))

    gc = grade_colour(overall)
    story.append(Paragraph(
        f'<font color="#{gc.hexval()[2:]}"><b>Overall Repository Grade: {grade}  ({overall}/100)</b></font>',
        styles["H2"]
    ))

    story.append(Spacer(1, 0.3*cm))
    story.append(Paragraph(
        f"Report generated: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')} | "
        f"GitHub Analyser v1.0",
        styles["Small"]
    ))
    story.append(PageBreak())

    # ─── CHARTS ──────────────────────────────────────────────────────────────
    charts_dir = Path(".") / "charts" / repo
    chart_files = {
        "score_radar": charts_dir / "score_radar.png",
        "commit_heatmap": charts_dir / "commit_heatmap.png",
        "commit_trend": charts_dir / "commit_trend.png",
        "contributors": charts_dir / "contributors.png",
        "languages": charts_dir / "languages.png",
        "issues_prs": charts_dir / "issues_prs.png",
    }

    def add_chart(key, title, width=16*cm):
        p = chart_files.get(key)
        if p and p.exists():
            story.append(Paragraph(title, styles["H2"]))
            story.append(Image(str(p), width=width, height=width * 0.45))
            story.append(Spacer(1, 0.3*cm))

    # Score radar
    if chart_files["score_radar"].exists():
        story.append(Paragraph("Score Radar", styles["H1"]))
        story.append(Image(str(chart_files["score_radar"]), width=10*cm, height=10*cm))
        story.append(Spacer(1, 0.5*cm))

    story.append(PageBreak())

    # ─── ACTIVITY ────────────────────────────────────────────────────────────
    story.append(Paragraph("1. Activity & Health", styles["H1"]))
    story.append(Paragraph(f"Score: {scores.get('activity', '—')}/100 | Grade: {score_to_grade(scores.get('activity', 0))}", styles["H2"]))
    add_chart("commit_heatmap", "52-Week Commit Heatmap", width=16*cm)
    add_chart("commit_trend", "Weekly Commit Trend (26 Weeks)", width=16*cm)
    add_chart("issues_prs", "Issues & Pull Requests", width=14*cm)
    story.append(PageBreak())

    # ─── CONTRIBUTORS ────────────────────────────────────────────────────────
    story.append(Paragraph("2. Community & Contributors", styles["H1"]))
    story.append(Paragraph(f"Score: {scores.get('community', '—')}/100 | Grade: {score_to_grade(scores.get('community', 0))}", styles["H2"]))
    add_chart("contributors", "Contributor Analysis", width=16*cm)

    # Bus factor
    top1 = summary.get("bus_factor_pct_top1", 0)
    top3 = summary.get("bus_factor_pct_top3", 0)
    bf_risk = "🚨 Critical" if top1 > 70 else ("⚠️ Moderate" if top3 > 80 else "✅ Healthy")
    story.append(Paragraph("Bus Factor Analysis", styles["H2"]))
    story.append(Paragraph(f"Top contributor: <b>{top1:.1f}%</b> of all commits", styles["Body"]))
    story.append(Paragraph(f"Top 3 contributors: <b>{top3:.1f}%</b> of all commits", styles["Body"]))
    story.append(Paragraph(f"Risk Level: <b>{bf_risk}</b>", styles["Body"]))
    story.append(Spacer(1, 0.3*cm))

    # Top contributors table
    tc = summary.get("top_contributors", [])
    if tc:
        story.append(Paragraph("Top Contributors", styles["H2"]))
        tc_data = [["Rank", "Username", "Commits", "Share %"]]
        for i, c in enumerate(tc[:10], 1):
            tc_data.append([str(i), c["login"], str(c["contributions"]), f"{c['pct']:.1f}%"])
        tc_table = Table(tc_data, colWidths=[1.5*cm, 6*cm, 3*cm, 3*cm])
        tc_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), C_ACCENT),
            ("TEXTCOLOR", (0, 0), (-1, 0), C_WHITE),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, -1), 9),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [HexColor("#f5f5f5"), C_WHITE]),
            ("GRID", (0, 0), (-1, -1), 0.3, C_GREY),
            ("TOPPADDING", (0, 0), (-1, -1), 5),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ("LEFTPADDING", (0, 0), (-1, -1), 6),
            ("ALIGN", (2, 0), (-1, -1), "CENTER"),
        ]))
        story.append(tc_table)

    story.append(PageBreak())

    # ─── CODE + SECURITY ─────────────────────────────────────────────────────
    story.append(Paragraph("3. Code Quality", styles["H1"]))
    story.append(Paragraph(f"Score: {scores.get('code_quality', '—')}/100 | Grade: {score_to_grade(scores.get('code_quality', 0))}", styles["H2"]))
    add_chart("languages", "Language Breakdown", width=10*cm)

    code_checks = {
        "has_tests": "Test directory present",
        "has_ci": "CI/CD configured",
        "has_docker": "Containerization (Docker)",
    }
    for key, label in code_checks.items():
        val = summary.get(key, False)
        icon = "✅" if val else "❌"
        story.append(Paragraph(f"{icon}  {label}", styles["Check"]))

    story.append(Spacer(1, 0.5*cm))
    story.append(Paragraph("4. Security Posture", styles["H1"]))
    story.append(Paragraph(f"Score: {scores.get('security', '—')}/100 | Grade: {score_to_grade(scores.get('security', 0))}", styles["H2"]))

    sec_checks = {
        "branch_protected": "Default branch is protected",
        "has_security": "SECURITY.md present",
    }
    for key, label in sec_checks.items():
        val = summary.get(key, False)
        icon = "✅" if val else "❌"
        story.append(Paragraph(f"{icon}  {label}", styles["Check"]))

    story.append(PageBreak())

    # ─── DOCS + RECOMMENDATIONS ──────────────────────────────────────────────
    story.append(Paragraph("5. Documentation & DX", styles["H1"]))
    story.append(Paragraph(f"Score: {scores.get('docs', '—')}/100 | Grade: {score_to_grade(scores.get('docs', 0))}", styles["H2"]))

    docs_checks = {
        "has_readme": "README.md present",
        "has_contributing": "CONTRIBUTING.md present",
        "has_coc": "CODE_OF_CONDUCT.md present",
        "has_changelog": "CHANGELOG.md present",
    }
    for key, label in docs_checks.items():
        val = summary.get(key, False)
        icon = "✅" if val else "❌"
        story.append(Paragraph(f"{icon}  {label}", styles["Check"]))

    story.append(Spacer(1, 0.8*cm))
    story.append(HRFlowable(width="100%", thickness=1, color=C_LIGHT))
    story.append(Spacer(1, 0.3*cm))
    story.append(Paragraph("Conclusion", styles["H1"]))
    story.append(Paragraph(
        f"<b>{owner}/{repo}</b> received an overall score of <b>{overall}/100</b> (Grade: {grade}). "
        f"This report was generated using GitHub's public API and represents a surface-level technical audit. "
        f"For production adoption decisions, supplement with manual code review and dynamic security testing.",
        styles["Body"]
    ))

    story.append(Spacer(1, 0.3*cm))
    story.append(Paragraph(
        f"<i>Generated by GitHub Analyser v1.0 | {datetime.now(timezone.utc).strftime('%Y-%m-%d')} | "
        f"Data sourced from GitHub API</i>",
        styles["Small"]
    ))

    # Build PDF
    doc = SimpleDocTemplate(
        str(out_path),
        pagesize=A4,
        rightMargin=2*cm, leftMargin=2*cm,
        topMargin=2*cm, bottomMargin=2*cm,
        title=f"GitHub Analysis: {owner}/{repo}",
        author="GitHub Analyser",
    )
    doc.build(story)
    print(f"\n✅ PDF report saved: {out_path}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("owner")
    parser.add_argument("repo")
    parser.add_argument("--data-dir", default=".")
    parser.add_argument("--scores", default=None, help='JSON string: \'{"code_quality":75,"activity":80,...}\'')
    parser.add_argument("--output", default=None)
    args = parser.parse_args()

    data = load_data(args.owner, args.repo, args.data_dir)

    # Default scores if not provided
    scores = {"code_quality": 50, "activity": 50, "community": 50, "security": 50, "docs": 50}
    if args.scores:
        try:
            scores.update(json.loads(args.scores))
        except json.JSONDecodeError as e:
            print(f"⚠️  Could not parse scores JSON: {e}")

    out_path = Path(args.output or f"GITHUB-REPORT-{args.repo}.pdf")
    build_report(args.owner, args.repo, data, scores, out_path)


if __name__ == "__main__":
    main()
