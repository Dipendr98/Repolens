---
name: gh-compare
description: Side-by-side comparison of two GitHub repositories across all dimensions — stars, activity, code quality, security, contributors, tech stack.
---

# GitHub Compare Skill

Compare two repositories head-to-head across all analysis dimensions.

## Input

`/github compare <url1> <url2>`

Parse both URLs to get `owner1/repo1` and `owner2/repo2`.

## Execution

Run all data fetches for BOTH repos in parallel (where possible). Collect identical metrics for each and present side-by-side.

## Comparison Dimensions

| Metric | Repo 1 | Repo 2 | Winner |
|---|---|---|---|
| ⭐ Stars | | | |
| 🍴 Forks | | | |
| 📅 Age | | | |
| 🔄 Last commit | | | |
| 📊 Commits/week | | | |
| 🐛 Open issues | | | |
| 🔀 Open PRs | | | |
| 👥 Contributors | | | |
| 🚌 Bus factor | | | |
| 🔒 Security score | | | |
| 📈 Activity score | | | |
| 🧪 Tests present | | | |
| 🤖 CI/CD | | | |
| 📄 License | | | |

## Overall Winner

Calculate overall score for each repo (using same scoring formula as `/github analyse`) and declare a winner with rationale.

## Use Cases to Mention

- "Choosing between two libraries"
- "Comparing your fork to upstream"
- "Evaluating alternatives before adopting a dependency"

## Output Format

1. Side-by-side comparison table
2. Score summary: Repo1 `XX/100` vs Repo2 `XX/100`
3. "Best for X" section — explain which is better for different use cases
4. Save to `GITHUB-COMPARE-{repo1}-vs-{repo2}.md`
