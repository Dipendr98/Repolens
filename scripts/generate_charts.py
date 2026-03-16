#!/usr/bin/env python3
"""
generate_charts.py — Generate all analysis charts for a GitHub repository.
Usage: python3 scripts/generate_charts.py <owner> <repo> [--type all|activity|contributors|score]
"""

import sys
import os
import json
import argparse
from pathlib import Path
from datetime import datetime, timedelta

try:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import matplotlib.patches as mpatches
    import numpy as np
except ImportError:
    print("Installing matplotlib and numpy...")
    os.system("pip install matplotlib numpy --break-system-packages -q")
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import matplotlib.patches as mpatches
    import numpy as np

# Colour palette
NAVY = "#1a1a2e"
BLUE = "#16213e"
ACCENT = "#0f3460"
GREEN = "#4CAF50"
RED = "#f44336"
ORANGE = "#FF9800"
YELLOW = "#FFC107"
PURPLE = "#9C27B0"
LIGHT = "#e0e0e0"
WHITE = "#ffffff"
GREY = "#888888"

GRADE_COLORS = {"A": GREEN, "B": "#8BC34A", "C": YELLOW, "D": ORANGE, "F": RED}


def load_data(owner, repo, data_dir="."):
    cache_file = Path(data_dir) / "cache" / f"{owner}_{repo}_data.json"
    if not cache_file.exists():
        print(f"⚠️  No cached data found at {cache_file}")
        print(f"   Run: python3 scripts/fetch_repo.py {owner} {repo}")
        sys.exit(1)
    with open(cache_file) as f:
        return json.load(f)


def setup_figure(figsize=(12, 6), bg=NAVY):
    fig = plt.figure(figsize=figsize, facecolor=bg)
    return fig


def score_to_grade(score):
    if score >= 90: return "A"
    if score >= 75: return "B"
    if score >= 60: return "C"
    if score >= 40: return "D"
    return "F"


def generate_commit_heatmap(data, out_dir):
    """52-week commit activity heatmap (GitHub-style)."""
    commit_activity = data.get("commit_activity", [])
    if not commit_activity:
        print("  ⚠️  No commit activity data")
        return

    fig = setup_figure((14, 4))
    ax = fig.add_subplot(111)
    ax.set_facecolor(NAVY)
    fig.patch.set_facecolor(NAVY)

    # Build 52x7 grid
    weeks = commit_activity[-52:] if len(commit_activity) >= 52 else commit_activity
    grid = []
    for week in weeks:
        days = week.get("days", [0] * 7)
        grid.append(days)

    grid_array = np.array(grid).T  # shape: (7, 52)
    max_val = grid_array.max() if grid_array.max() > 0 else 1

    # Draw cells
    cell_size = 0.85
    for col_i, day_counts in enumerate(grid):
        for row_i, count in enumerate(day_counts):
            intensity = count / max_val
            if count == 0:
                colour = "#161b22"
            elif intensity < 0.25:
                colour = "#0e4429"
            elif intensity < 0.5:
                colour = "#006d32"
            elif intensity < 0.75:
                colour = "#26a641"
            else:
                colour = "#39d353"
            rect = plt.Rectangle((col_i, 6 - row_i), cell_size, cell_size,
                                  facecolor=colour, edgecolor=NAVY, linewidth=0.5)
            ax.add_patch(rect)

    # Axis labels
    day_labels = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]
    for i, label in enumerate(day_labels):
        ax.text(-1.2, 6.4 - i, label, color=LIGHT, fontsize=7, va="center", ha="right")

    # Month labels
    today = datetime.now()
    for i, week_data in enumerate(weeks):
        week_ts = week_data.get("week", 0)
        if week_ts:
            dt = datetime.fromtimestamp(week_ts)
            if dt.day <= 7:
                ax.text(i, 7.5, dt.strftime("%b"), color=GREY, fontsize=7, ha="center")

    ax.set_xlim(-1.5, len(weeks) + 0.5)
    ax.set_ylim(-0.5, 8.5)
    ax.axis("off")

    # Title
    summary = data.get("summary", {})
    total = sum(w.get("total", 0) for w in weeks)
    ax.set_title(f"📈 Commit Activity — {summary.get('full_name', '')}  |  {total:,} commits in last 52 weeks",
                 color=WHITE, fontsize=12, pad=15, loc="left")

    # Legend
    legend_items = [
        mpatches.Patch(facecolor="#161b22", label="0"),
        mpatches.Patch(facecolor="#0e4429", label="1-25%"),
        mpatches.Patch(facecolor="#26a641", label="26-75%"),
        mpatches.Patch(facecolor="#39d353", label="76-100%"),
    ]
    ax.legend(handles=legend_items, loc="lower right", ncol=4,
              framealpha=0, labelcolor=LIGHT, fontsize=7)

    plt.tight_layout()
    out_path = out_dir / "commit_heatmap.png"
    plt.savefig(out_path, dpi=150, bbox_inches="tight", facecolor=NAVY)
    plt.close()
    print(f"  ✅ Saved: {out_path}")


def generate_commit_trend(data, out_dir):
    """Weekly commit trend line chart."""
    commit_activity = data.get("commit_activity", [])
    if not commit_activity:
        return

    weeks = commit_activity[-26:]  # last 26 weeks
    totals = [w.get("total", 0) for w in weeks]
    labels = [f"W{i+1}" for i in range(len(weeks))]

    fig = setup_figure((12, 4))
    ax = fig.add_subplot(111)
    ax.set_facecolor(BLUE)
    fig.patch.set_facecolor(NAVY)

    x = np.arange(len(totals))
    ax.fill_between(x, totals, alpha=0.3, color=GREEN)
    ax.plot(x, totals, color=GREEN, linewidth=2, marker="o", markersize=3)

    # Moving average
    if len(totals) >= 4:
        ma = np.convolve(totals, np.ones(4)/4, mode="valid")
        ax.plot(np.arange(3, len(totals)), ma, color=YELLOW, linewidth=1.5,
                linestyle="--", alpha=0.8, label="4-week avg")

    ax.set_xticks(x[::2])
    ax.set_xticklabels(labels[::2], color=GREY, fontsize=8)
    ax.tick_params(axis="y", colors=GREY)
    ax.spines[:].set_color(ACCENT)
    ax.set_facecolor(BLUE)

    summary = data.get("summary", {})
    ax.set_title(f"Weekly Commit Trend — Last 26 Weeks", color=WHITE, fontsize=11, pad=10, loc="left")
    ax.set_ylabel("Commits", color=GREY, fontsize=9)
    ax.legend(framealpha=0, labelcolor=LIGHT, fontsize=8)
    ax.grid(axis="y", alpha=0.2, color=GREY)

    plt.tight_layout()
    out_path = out_dir / "commit_trend.png"
    plt.savefig(out_path, dpi=150, bbox_inches="tight", facecolor=NAVY)
    plt.close()
    print(f"  ✅ Saved: {out_path}")


def generate_contributor_charts(data, out_dir):
    """Contributor pie + bar charts."""
    contributors = data.get("summary", {}).get("top_contributors", [])
    if not contributors:
        return

    top = contributors[:8]
    names = [c["login"] for c in top]
    pcts = [c["pct"] for c in top]

    colors = [GREEN, "#2196F3", "#FF9800", PURPLE, "#00BCD4",
              "#FF5722", "#8BC34A", "#795548"]

    # Pie chart
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6), facecolor=NAVY)

    wedges, texts, autotexts = ax1.pie(
        pcts, labels=None, autopct="%1.1f%%", colors=colors[:len(top)],
        startangle=90, pctdistance=0.8, wedgeprops=dict(width=0.6, edgecolor=NAVY)
    )
    for at in autotexts:
        at.set_color(WHITE)
        at.set_fontsize(8)

    ax1.legend(wedges, names, loc="lower center", ncol=2, bbox_to_anchor=(0.5, -0.15),
               framealpha=0, labelcolor=LIGHT, fontsize=9)
    ax1.set_facecolor(NAVY)
    ax1.set_title("Contribution Share (Top 8)", color=WHITE, fontsize=11, pad=10)

    # Bar chart
    ax2.set_facecolor(BLUE)
    bar_names = [c["login"] for c in contributors[:10]]
    bar_commits = [c["contributions"] for c in contributors[:10]]
    y = np.arange(len(bar_names))
    bars = ax2.barh(y, bar_commits, color=colors[:len(bar_names)], edgecolor=NAVY, height=0.7)
    ax2.set_yticks(y)
    ax2.set_yticklabels(bar_names, color=LIGHT, fontsize=9)
    ax2.tick_params(axis="x", colors=GREY)
    ax2.spines[:].set_color(ACCENT)
    ax2.set_title("Top Contributors by Commits", color=WHITE, fontsize=11, pad=10)
    ax2.set_xlabel("Commits", color=GREY, fontsize=9)
    ax2.grid(axis="x", alpha=0.2, color=GREY)

    # Value labels on bars
    for bar, val in zip(bars, bar_commits):
        ax2.text(val + max(bar_commits) * 0.01, bar.get_y() + bar.get_height() / 2,
                 f"{val:,}", color=LIGHT, va="center", fontsize=8)

    fig.suptitle(f"Contributor Analysis", color=WHITE, fontsize=13, y=1.02)
    plt.tight_layout()
    out_path = out_dir / "contributors.png"
    plt.savefig(out_path, dpi=150, bbox_inches="tight", facecolor=NAVY)
    plt.close()
    print(f"  ✅ Saved: {out_path}")


def generate_language_chart(data, out_dir):
    """Language breakdown donut chart."""
    lang_pct = data.get("summary", {}).get("language_breakdown", {})
    if not lang_pct:
        return

    langs = list(lang_pct.keys())[:8]
    pcts = [lang_pct[l] for l in langs]

    colors = ["#3178C6", "#F7DF1E", "#3572A5", "#e34c26", "#563d7c",
              "#00ADD8", "#b07219", "#4F5D95"]

    fig = setup_figure((8, 6))
    ax = fig.add_subplot(111)
    ax.set_facecolor(NAVY)

    wedges, texts = ax.pie(pcts, labels=None, colors=colors[:len(langs)],
                           startangle=90, wedgeprops=dict(width=0.55, edgecolor=NAVY))

    # Centre text
    total_top = sum(pcts)
    ax.text(0, 0, f"{len(langs)}\nLangs", ha="center", va="center",
            color=WHITE, fontsize=14, fontweight="bold")

    ax.legend(wedges,
              [f"{l} ({p:.1f}%)" for l, p in zip(langs, pcts)],
              loc="lower center", ncol=2, bbox_to_anchor=(0.5, -0.15),
              framealpha=0, labelcolor=LIGHT, fontsize=9)

    ax.set_title("Language Breakdown", color=WHITE, fontsize=12, pad=10)
    plt.tight_layout()
    out_path = out_dir / "languages.png"
    plt.savefig(out_path, dpi=150, bbox_inches="tight", facecolor=NAVY)
    plt.close()
    print(f"  ✅ Saved: {out_path}")


def generate_score_radar(scores, owner, repo, out_dir):
    """Radar chart of all 5 dimension scores."""
    dimensions = ["Code\nQuality", "Activity\n& Health", "Community", "Security", "Docs\n& DX"]
    values = [
        scores.get("code_quality", 50),
        scores.get("activity", 50),
        scores.get("community", 50),
        scores.get("security", 50),
        scores.get("docs", 50),
    ]

    # Close the radar
    values += values[:1]
    N = len(dimensions)
    angles = [n / float(N) * 2 * np.pi for n in range(N)]
    angles += angles[:1]

    fig = setup_figure((8, 8))
    ax = fig.add_subplot(111, polar=True)
    ax.set_facecolor(BLUE)
    fig.patch.set_facecolor(NAVY)

    # Background circles
    for r in [20, 40, 60, 80, 100]:
        ax.plot(angles, [r] * len(angles), color=GREY, alpha=0.2, linewidth=0.5)
        ax.text(0, r, str(r), color=GREY, fontsize=7, ha="center", va="center")

    ax.fill(angles, values, color=GREEN, alpha=0.25)
    ax.plot(angles, values, color=GREEN, linewidth=2)
    ax.scatter(angles[:-1], values[:-1], color=GREEN, s=60, zorder=5)

    # Labels
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(dimensions, color=WHITE, fontsize=10)
    ax.set_ylim(0, 100)
    ax.set_yticks([])
    ax.spines["polar"].set_color(ACCENT)
    ax.grid(alpha=0.2)

    # Score annotations
    for angle, val, dim in zip(angles[:-1], values[:-1], dimensions):
        ax.annotate(f"{val}", xy=(angle, val), xytext=(angle, val + 8),
                    color=YELLOW, fontsize=9, ha="center", fontweight="bold")

    overall = round(sum(values[:-1]) / len(dimensions))
    grade = score_to_grade(overall)
    ax.set_title(f"{owner}/{repo}\nOverall Score: {overall}/100  [{grade}]",
                 color=WHITE, fontsize=12, pad=20)

    plt.tight_layout()
    out_path = out_dir / "score_radar.png"
    plt.savefig(out_path, dpi=150, bbox_inches="tight", facecolor=NAVY)
    plt.close()
    print(f"  ✅ Saved: {out_path}")


def generate_issue_pr_chart(data, out_dir):
    """Open vs closed issues/PRs bar chart."""
    issues = data.get("issues", [])
    pulls = data.get("pulls", [])

    if not issues and not pulls:
        return

    issue_open = len([i for i in issues if i.get("state") == "open" and "pull_request" not in i])
    issue_closed = len([i for i in issues if i.get("state") == "closed" and "pull_request" not in i])
    pr_open = len([p for p in pulls if p.get("state") == "open"])
    pr_closed = len([p for p in pulls if p.get("state") == "closed"])

    fig = setup_figure((10, 5))
    ax = fig.add_subplot(111)
    ax.set_facecolor(BLUE)
    fig.patch.set_facecolor(NAVY)

    categories = ["Issues\n(Open)", "Issues\n(Closed)", "PRs\n(Open)", "PRs\n(Closed/Merged)"]
    counts = [issue_open, issue_closed, pr_open, pr_closed]
    colors_ = [RED, GREEN, ORANGE, GREEN]

    bars = ax.bar(categories, counts, color=colors_, edgecolor=NAVY, width=0.5)
    for bar, val in zip(bars, counts):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.5,
                str(val), color=WHITE, ha="center", fontsize=11, fontweight="bold")

    ax.set_facecolor(BLUE)
    ax.tick_params(colors=LIGHT)
    ax.spines[:].set_color(ACCENT)
    ax.set_title("Issues & Pull Requests Overview", color=WHITE, fontsize=12, pad=10, loc="left")
    ax.set_ylabel("Count", color=GREY, fontsize=9)
    ax.grid(axis="y", alpha=0.2, color=GREY)

    plt.tight_layout()
    out_path = out_dir / "issues_prs.png"
    plt.savefig(out_path, dpi=150, bbox_inches="tight", facecolor=NAVY)
    plt.close()
    print(f"  ✅ Saved: {out_path}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("owner")
    parser.add_argument("repo")
    parser.add_argument("--type", default="all", choices=["all", "activity", "contributors", "score", "language"])
    parser.add_argument("--data-dir", default=".")
    parser.add_argument("--scores", default=None, help="JSON string of scores e.g. '{\"code_quality\":75,...}'")
    args = parser.parse_args()

    data = load_data(args.owner, args.repo, args.data_dir)
    out_dir = Path(args.data_dir) / "charts" / args.repo
    out_dir.mkdir(parents=True, exist_ok=True)

    print(f"\n📊 Generating charts for {args.owner}/{args.repo}...\n")

    chart_type = args.type

    if chart_type in ("all", "activity"):
        print("  🗓️  Commit heatmap...")
        generate_commit_heatmap(data, out_dir)
        print("  📈 Commit trend...")
        generate_commit_trend(data, out_dir)
        print("  🐛 Issues & PRs...")
        generate_issue_pr_chart(data, out_dir)

    if chart_type in ("all", "contributors"):
        print("  👥 Contributors...")
        generate_contributor_charts(data, out_dir)

    if chart_type in ("all", "language"):
        print("  🔤 Languages...")
        generate_language_chart(data, out_dir)

    if chart_type in ("all", "score") and args.scores:
        try:
            import json as json_
            scores = json_.loads(args.scores)
            print("  🎯 Score radar...")
            generate_score_radar(scores, args.owner, args.repo, out_dir)
        except Exception as e:
            print(f"  ⚠️  Could not generate radar: {e}")

    print(f"\n✅ All charts saved to {out_dir}/")


if __name__ == "__main__":
    main()
