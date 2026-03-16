#!/usr/bin/env python3
"""
fetch_repo.py — Fetch GitHub repository data and cache locally.
Usage: python3 scripts/fetch_repo.py <owner> <repo> [--token TOKEN]
"""

import sys
import os
import json
import argparse
import time
from datetime import datetime, timezone
from pathlib import Path

try:
    import requests
except ImportError:
    print("Installing requests...")
    os.system("pip install requests --break-system-packages -q")
    import requests


def get_headers(token=None):
    headers = {"Accept": "application/vnd.github+json", "X-GitHub-Api-Version": "2022-11-28"}
    token = token or os.environ.get("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"
    return headers


def fetch(url, headers, label=""):
    try:
        r = requests.get(url, headers=headers, timeout=15)
        if r.status_code == 200:
            return r.json()
        elif r.status_code == 404:
            return None
        elif r.status_code == 403:
            print(f"  ⚠️  Rate limited or forbidden: {label}")
            return None
        else:
            return None
    except Exception as e:
        print(f"  ❌ Error fetching {label}: {e}")
        return None


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("owner")
    parser.add_argument("repo")
    parser.add_argument("--token", default=None)
    parser.add_argument("--output-dir", default=".")
    args = parser.parse_args()

    owner, repo = args.owner, args.repo
    headers = get_headers(args.token)
    base = f"https://api.github.com/repos/{owner}/{repo}"

    print(f"\n🔍 Fetching data for {owner}/{repo}...\n")

    data = {}

    # Core repo info
    print("  📦 Core metadata...")
    data["repo"] = fetch(base, headers, "repo")
    if not data["repo"]:
        print(f"❌ Repository {owner}/{repo} not found or inaccessible.")
        sys.exit(1)

    # Languages
    print("  🔤 Languages...")
    data["languages"] = fetch(f"{base}/languages", headers, "languages") or {}

    # Contributors
    print("  👥 Contributors...")
    data["contributors"] = fetch(f"{base}/contributors?per_page=100&anon=true", headers, "contributors") or []

    # Commit activity (52 weeks)
    print("  📈 Commit activity (52 weeks)...")
    data["commit_activity"] = fetch(f"{base}/stats/commit_activity", headers, "commit_activity") or []

    # Participation
    print("  📊 Participation stats...")
    data["participation"] = fetch(f"{base}/stats/participation", headers, "participation") or {}

    # Issues (recent 100)
    print("  🐛 Issues...")
    data["issues"] = fetch(f"{base}/issues?state=all&per_page=100&sort=created&direction=desc", headers, "issues") or []

    # Pull requests (recent 50)
    print("  🔀 Pull requests...")
    data["pulls"] = fetch(f"{base}/pulls?state=all&per_page=50", headers, "pulls") or []

    # Releases
    print("  🏷️  Releases...")
    data["releases"] = fetch(f"{base}/releases?per_page=10", headers, "releases") or []

    # Root contents
    print("  📁 Root file tree...")
    data["contents"] = fetch(f"{base}/contents", headers, "contents") or []

    # Community profile
    print("  🏘️  Community profile...")
    data["community"] = fetch(f"{base}/community/profile", headers, "community") or {}

    # Workflows
    print("  🤖 CI/CD workflows...")
    data["workflows"] = fetch(f"{base}/contents/.github/workflows", headers, "workflows") or []

    # Default branch info
    default_branch = data["repo"].get("default_branch", "main")
    print(f"  🌿 Branch protection ({default_branch})...")
    data["branch_protection"] = fetch(f"{base}/branches/{default_branch}", headers, "branch_protection") or {}

    # Topics
    data["topics"] = data["repo"].get("topics", [])

    # Computed summary
    total_lang_bytes = sum(data["languages"].values())
    lang_pct = {
        lang: round(bytes_ / total_lang_bytes * 100, 1)
        for lang, bytes_ in sorted(data["languages"].items(), key=lambda x: -x[1])
    } if total_lang_bytes > 0 else {}

    total_contributions = sum(c.get("contributions", 0) for c in data["contributors"])
    top_contributors = sorted(data["contributors"], key=lambda x: x.get("contributions", 0), reverse=True)[:10]
    top1_pct = (top_contributors[0]["contributions"] / total_contributions * 100) if total_contributions > 0 else 0
    top3_pct = (sum(c["contributions"] for c in top_contributors[:3]) / total_contributions * 100) if total_contributions > 0 else 0

    weekly_commits = [w.get("total", 0) for w in (data["commit_activity"] or [])]
    commits_30d = sum(weekly_commits[-4:]) if len(weekly_commits) >= 4 else sum(weekly_commits)
    commits_90d = sum(weekly_commits[-13:]) if len(weekly_commits) >= 13 else sum(weekly_commits)
    recent_nonzero = [w for w in weekly_commits[-12:] if w > 0]
    avg_commits_week = round(sum(recent_nonzero) / len(recent_nonzero), 1) if recent_nonzero else 0

    # Check key files
    root_files = [f["name"].lower() for f in data["contents"] if isinstance(data["contents"], list)]
    has_tests = any(name in root_files for name in ["test", "tests", "__tests__", "spec", "specs"])
    has_docker = "dockerfile" in root_files or "docker-compose.yml" in root_files
    has_contributing = "contributing.md" in root_files
    has_coc = "code_of_conduct.md" in root_files
    has_security = "security.md" in root_files
    has_changelog = "changelog.md" in root_files
    has_readme = "readme.md" in root_files or "readme" in root_files

    data["summary"] = {
        "owner": owner,
        "repo": repo,
        "full_name": f"{owner}/{repo}",
        "description": data["repo"].get("description", ""),
        "stars": data["repo"].get("stargazers_count", 0),
        "forks": data["repo"].get("forks_count", 0),
        "watchers": data["repo"].get("watchers_count", 0),
        "open_issues": data["repo"].get("open_issues_count", 0),
        "primary_language": data["repo"].get("language", "Unknown"),
        "language_breakdown": lang_pct,
        "license": (data["repo"].get("license") or {}).get("name", "No license"),
        "created_at": data["repo"].get("created_at", ""),
        "pushed_at": data["repo"].get("pushed_at", ""),
        "archived": data["repo"].get("archived", False),
        "homepage": data["repo"].get("homepage", ""),
        "topics": data["topics"],
        "total_contributors": len(data["contributors"]),
        "bus_factor_pct_top1": round(top1_pct, 1),
        "bus_factor_pct_top3": round(top3_pct, 1),
        "top_contributors": [
            {"login": c.get("login", "anon"), "contributions": c.get("contributions", 0),
             "pct": round(c.get("contributions", 0) / total_contributions * 100, 1) if total_contributions > 0 else 0}
            for c in top_contributors
        ],
        "commits_last_30d": commits_30d,
        "commits_last_90d": commits_90d,
        "avg_commits_per_week": avg_commits_week,
        "releases_count": len(data["releases"]),
        "latest_release": data["releases"][0].get("tag_name", "No releases") if data["releases"] else "No releases",
        "has_tests": has_tests,
        "has_docker": has_docker,
        "has_contributing": has_contributing,
        "has_coc": has_coc,
        "has_security": has_security,
        "has_changelog": has_changelog,
        "has_readme": has_readme,
        "has_ci": len(data["workflows"]) > 0 if isinstance(data["workflows"], list) else False,
        "branch_protected": bool((data["branch_protection"].get("protection") or {}).get("enabled")),
        "default_branch": default_branch,
        "fetched_at": datetime.now(timezone.utc).isoformat(),
    }

    # Save to cache
    out_dir = Path(args.output_dir) / "cache"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_file = out_dir / f"{owner}_{repo}_data.json"
    with open(out_file, "w") as f:
        json.dump(data, f, indent=2, default=str)

    print(f"\n✅ Data fetched and saved to {out_file}")
    print(f"\n📊 Quick Summary:")
    print(f"   ⭐ {data['summary']['stars']:,} stars  |  🍴 {data['summary']['forks']:,} forks")
    print(f"   👥 {data['summary']['total_contributors']} contributors  |  🐛 {data['summary']['open_issues']} open issues")
    print(f"   📈 {commits_30d} commits in last 30 days  |  avg {avg_commits_week}/week")
    print(f"   🔤 Primary: {data['summary']['primary_language']}")
    print(f"   📄 License: {data['summary']['license']}")

    return str(out_file)


if __name__ == "__main__":
    main()
